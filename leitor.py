from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
import re
import tempfile
from typing import Any
from zipfile import BadZipFile, ZipFile

from validacoes import FORMATOS_IMAGEM, validar_arquivo


def _chave_natural(nome: str) -> list[int | str]:
    return [int(parte) if parte.isdigit() else parte.casefold() for parte in re.split(r"(\d+)", nome)]


def _nomes_imagens(nomes: list[str]) -> list[str]:
    paginas = [nome for nome in nomes if Path(nome).suffix.lower() in FORMATOS_IMAGEM]
    return sorted(paginas, key=_chave_natural)


class LeitorArquivo(ABC):
    def __init__(self, caminho: str | Path) -> None:
        self.caminho = validar_arquivo(caminho)
        self._aberto = False

    @abstractmethod
    def abrir(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def obter_pagina(self, numero: int) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def total_paginas(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def fechar(self) -> None:
        raise NotImplementedError

    def _validar_numero_pagina(self, numero: int) -> None:
        if numero < 0 or numero >= self.total_paginas:
            raise ValueError("Página fora dos limites da obra.")


class LeitorPDF(LeitorArquivo):
    def __init__(self, caminho: str | Path) -> None:
        super().__init__(caminho)
        self._documento: Any = None

    def abrir(self) -> None:
        try:
            import fitz

            self._documento = fitz.open(self.caminho)
            if self._documento.page_count == 0:
                raise ValueError("O PDF não possui páginas.")
            self._aberto = True
        except ImportError as erro:
            raise RuntimeError("Instale a dependência PyMuPDF para ler arquivos PDF.") from erro
        except Exception as erro:
            raise ValueError(f"Não foi possível abrir o PDF: {erro}") from erro

    @property
    def total_paginas(self) -> int:
        return self._documento.page_count if self._documento else 0

    def obter_pagina(self, numero: int) -> Any:
        if not self._aberto:
            self.abrir()
        self._validar_numero_pagina(numero)
        try:
            from PIL import Image

            pagina = self._documento.load_page(numero)
            pixmap = pagina.get_pixmap(matrix=self._matriz_renderizacao(), alpha=False)
            return Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        except ImportError as erro:
            raise RuntimeError("Instale a dependência Pillow para exibir páginas.") from erro

    @staticmethod
    def _matriz_renderizacao() -> Any:
        import fitz

        return fitz.Matrix(1.6, 1.6)

    def fechar(self) -> None:
        if self._documento:
            self._documento.close()
        self._documento = None
        self._aberto = False


class LeitorCBZ(LeitorArquivo):
    def __init__(self, caminho: str | Path) -> None:
        super().__init__(caminho)
        self._arquivo: ZipFile | None = None
        self._paginas: list[str] = []

    def abrir(self) -> None:
        try:
            self._arquivo = ZipFile(self.caminho)
            self._paginas = _nomes_imagens(self._arquivo.namelist())
            if not self._paginas:
                raise ValueError("O arquivo CBZ não contém imagens.")
            self._aberto = True
        except (BadZipFile, OSError) as erro:
            raise ValueError(f"Não foi possível abrir o CBZ: {erro}") from erro

    @property
    def total_paginas(self) -> int:
        return len(self._paginas)

    def obter_pagina(self, numero: int) -> Any:
        if not self._aberto:
            self.abrir()
        self._validar_numero_pagina(numero)
        from PIL import Image

        if self._arquivo is None:
            raise RuntimeError("O arquivo CBZ não está aberto.")
        with self._arquivo.open(self._paginas[numero]) as pagina:
            imagem = Image.open(BytesIO(pagina.read()))
            imagem.load()
            return imagem.convert("RGB")

    def fechar(self) -> None:
        if self._arquivo:
            self._arquivo.close()
        self._arquivo = None
        self._paginas = []
        self._aberto = False


class LeitorCBR(LeitorArquivo):
    def __init__(self, caminho: str | Path) -> None:
        super().__init__(caminho)
        self._arquivo: Any = None
        self._paginas: list[str] = []

    def abrir(self) -> None:
        try:
            import rarfile

            self._arquivo = rarfile.RarFile(self.caminho)
            self._paginas = _nomes_imagens(self._arquivo.namelist())
            if not self._paginas:
                raise ValueError("O arquivo CBR não contém imagens.")
            self._aberto = True
        except ImportError as erro:
            raise RuntimeError("Instale a dependência rarfile para ler arquivos CBR.") from erro
        except Exception as erro:
            raise ValueError(
                "Não foi possível abrir o CBR. Verifique se o arquivo é válido e se "
                f"UnRAR, 7-Zip ou bsdtar está instalado. Detalhes: {erro}"
            ) from erro

    @property
    def total_paginas(self) -> int:
        return len(self._paginas)

    def obter_pagina(self, numero: int) -> Any:
        if not self._aberto:
            self.abrir()
        self._validar_numero_pagina(numero)
        from PIL import Image

        try:
            dados = self._arquivo.read(self._paginas[numero])
            imagem = Image.open(BytesIO(dados))
            imagem.load()
            return imagem.convert("RGB")
        except Exception as erro:
            raise ValueError(f"Não foi possível extrair a página do CBR: {erro}") from erro

    def fechar(self) -> None:
        if self._arquivo:
            self._arquivo.close()
        self._arquivo = None
        self._paginas = []
        self._aberto = False


class LeitorCB7(LeitorArquivo):
    def __init__(self, caminho: str | Path) -> None:
        super().__init__(caminho)
        self._temporario: tempfile.TemporaryDirectory[str] | None = None
        self._paginas: list[Path] = []

    def abrir(self) -> None:
        try:
            import py7zr

            self._temporario = tempfile.TemporaryDirectory(prefix="bookreadnet_cb7_")
            destino = Path(self._temporario.name)
            with py7zr.SevenZipFile(self.caminho, mode="r") as arquivo:
                arquivo.extractall(path=destino)
            self._paginas = sorted(
                [item for item in destino.rglob("*") if item.is_file() and item.suffix.lower() in FORMATOS_IMAGEM],
                key=lambda item: _chave_natural(str(item.relative_to(destino))),
            )
            if not self._paginas:
                self.fechar()
                raise ValueError("O arquivo CB7 não contém imagens.")
            self._aberto = True
        except ImportError as erro:
            self.fechar()
            raise RuntimeError("Instale a dependência py7zr para ler arquivos CB7.") from erro
        except Exception as erro:
            self.fechar()
            if isinstance(erro, ValueError):
                raise
            raise ValueError(f"Não foi possível abrir o CB7: {erro}") from erro

    @property
    def total_paginas(self) -> int:
        return len(self._paginas)

    def obter_pagina(self, numero: int) -> Any:
        if not self._aberto:
            self.abrir()
        self._validar_numero_pagina(numero)
        from PIL import Image

        with Image.open(self._paginas[numero]) as imagem:
            return imagem.convert("RGB")

    def fechar(self) -> None:
        self._paginas = []
        if self._temporario:
            self._temporario.cleanup()
        self._temporario = None
        self._aberto = False


class FabricaLeitores:
    _leitores = {
        ".pdf": LeitorPDF,
        ".cbz": LeitorCBZ,
        ".cbr": LeitorCBR,
        ".cb7": LeitorCB7,
    }

    @classmethod
    def criar(cls, caminho: str | Path) -> LeitorArquivo:
        arquivo = validar_arquivo(caminho)
        classe = cls._leitores.get(arquivo.suffix.lower())
        if classe is None:
            raise ValueError("Não existe leitor para esse formato.")
        leitor = classe(arquivo)
        leitor.abrir()
        return leitor
