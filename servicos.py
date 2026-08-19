from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any
from uuid import uuid4

from leitor import FabricaLeitores, LeitorArquivo
from modelos import HQ, Manga, LivroDigital, ObraDigital, StatusLeitura, Usuario
from persistencia import RepositorioJSON
from validacoes import validar_arquivo, validar_capa, validar_titulo


class BibliotecaDigital:
    TIPOS_OBRA = {"HQ": HQ, "Mangá": Manga, "Livro digital": LivroDigital}

    def __init__(self, nome: str, pasta_base: str | Path | None = None) -> None:
        self.nome = nome.strip() or "BookReadNet"
        self.pasta_base = Path(pasta_base or Path(__file__).parent).resolve()
        self.pasta_arquivos = self.pasta_base / "biblioteca" / "arquivos"
        self.pasta_capas = self.pasta_base / "biblioteca" / "capas"
        self.pasta_dados = self.pasta_base / "dados"
        self.pasta_arquivos.mkdir(parents=True, exist_ok=True)
        self.pasta_capas.mkdir(parents=True, exist_ok=True)
        self.repositorio = RepositorioJSON(self.pasta_dados / "bookreadnet.json")
        self.__obras, self.usuario = self.repositorio.carregar()

    @property
    def obras(self) -> list[ObraDigital]:
        return list(self.__obras)

    def cadastrar_obra(
        self,
        tipo: str,
        titulo: str,
        autor: str,
        caminho_arquivo: str,
        categoria: str = "Sem categoria",
        serie: str = "",
        editora: str = "",
        idioma: str = "Português",
        caminho_capa: str = "",
        copiar_arquivo: bool = True,
        **dados_especificos: Any,
    ) -> ObraDigital:
        titulo = validar_titulo(titulo)
        origem = validar_arquivo(caminho_arquivo)
        classe = self.TIPOS_OBRA.get(tipo)
        if classe is None:
            raise ValueError("Selecione um tipo de obra válido.")

        id_obra = uuid4().hex[:10].upper()
        destino = self._copiar_para_biblioteca(origem, self.pasta_arquivos, id_obra) if copiar_arquivo else origem
        destino_capa = ""
        try:
            if caminho_capa:
                capa = validar_capa(caminho_capa)
                destino_capa = str(self._copiar_para_biblioteca(capa, self.pasta_capas, id_obra))
            obra = classe(
                id_obra=id_obra,
                titulo=titulo,
                autor=autor,
                caminho_arquivo=str(destino),
                categoria=categoria,
                serie=serie,
                editora=editora,
                idioma=idioma,
                caminho_capa=destino_capa,
                **dados_especificos,
            )
            self._validar_duplicidade(obra)
            self.__obras.append(obra)
            self.salvar()
            return obra
        except Exception:
            if copiar_arquivo and destino.exists():
                destino.unlink(missing_ok=True)
            if destino_capa:
                Path(destino_capa).unlink(missing_ok=True)
            raise

    def editar_obra(self, id_obra: str, **alteracoes: Any) -> ObraDigital:
        obra = self.buscar_por_id(id_obra)
        campos_editaveis = {"titulo", "autor", "categoria", "serie", "editora", "idioma"}
        for campo, valor in alteracoes.items():
            if campo in campos_editaveis or hasattr(obra, campo):
                setattr(obra, campo, valor)
        self._validar_duplicidade(obra, ignorar_id=obra.id_obra)
        self.salvar()
        return obra

    def excluir_obra(self, id_obra: str, excluir_arquivo: bool = False) -> ObraDigital:
        obra = self.buscar_por_id(id_obra)
        self.__obras.remove(obra)
        self.usuario.remover_dados_obra(id_obra)
        self.salvar()
        if excluir_arquivo:
            self._excluir_arquivo_gerenciado(obra.caminho_arquivo, self.pasta_arquivos)
            if obra.caminho_capa:
                self._excluir_arquivo_gerenciado(obra.caminho_capa, self.pasta_capas)
        return obra

    def buscar_por_id(self, id_obra: str) -> ObraDigital:
        for obra in self.__obras:
            if obra.id_obra == id_obra:
                return obra
        raise ValueError("Obra não encontrada.")

    def pesquisar(self, termo: str = "") -> list[ObraDigital]:
        termo = termo.strip().casefold()
        if not termo:
            return self.obras
        return [
            obra
            for obra in self.__obras
            if termo in obra.titulo.casefold()
            or termo in obra.autor.casefold()
            or termo in obra.categoria.casefold()
            or termo in obra.serie.casefold()
        ]

    def filtrar(
        self,
        termo: str = "",
        tipo: str = "Todos",
        status: str = "Todos",
        somente_favoritos: bool = False,
    ) -> list[ObraDigital]:
        obras = self.pesquisar(termo)
        if tipo != "Todos":
            obras = [obra for obra in obras if obra.obter_tipo() == tipo]
        if status != "Todos":
            obras = [obra for obra in obras if obra.status_leitura.value == status]
        if somente_favoritos:
            obras = [obra for obra in obras if obra.favorito]
        return sorted(obras, key=lambda obra: obra.titulo.casefold())

    def alternar_favorito(self, id_obra: str) -> bool:
        obra = self.buscar_por_id(id_obra)
        obra.favorito = not obra.favorito
        self.salvar()
        return obra.favorito

    def criar_leitor(self, id_obra: str) -> LeitorArquivo:
        obra = self.buscar_por_id(id_obra)
        return FabricaLeitores.criar(obra.caminho_arquivo)

    def obter_progresso(self, id_obra: str):
        self.buscar_por_id(id_obra)
        return self.usuario.obter_progresso(id_obra)

    def salvar_progresso(self, id_obra: str, pagina: int, total_paginas: int):
        obra = self.buscar_por_id(id_obra)
        progresso = self.usuario.salvar_progresso(id_obra, pagina, total_paginas)
        obra.numero_paginas = total_paginas
        obra.status_leitura = progresso.status
        self.salvar()
        return progresso

    def continuar_lendo(self) -> list[ObraDigital]:
        progressos = self.usuario.progressos
        candidatas = [
            obra
            for obra in self.__obras
            if obra.id_obra in progressos and progressos[obra.id_obra].pagina_atual > 0
        ]
        return sorted(
            candidatas,
            key=lambda obra: progressos[obra.id_obra].ultima_leitura or "",
            reverse=True,
        )

    def listar_historico(self) -> list[str]:
        linhas: list[str] = []
        for item in reversed(self.usuario.historico):
            try:
                titulo = self.buscar_por_id(item.obra_id).titulo
            except ValueError:
                continue
            data = item.data.replace("T", " ")[:16]
            linhas.append(f"{data} | {titulo} | página {item.pagina}")
        return linhas

    def categorias(self) -> list[str]:
        return sorted({obra.categoria for obra in self.__obras}, key=str.casefold)

    def salvar(self) -> None:
        self.repositorio.salvar(self.__obras, self.usuario)

    def _validar_duplicidade(self, nova_obra: ObraDigital, ignorar_id: str | None = None) -> None:
        for obra in self.__obras:
            if obra.id_obra == ignorar_id:
                continue
            mesma_base = (
                obra.titulo.casefold() == nova_obra.titulo.casefold()
                and obra.autor.casefold() == nova_obra.autor.casefold()
                and obra.obter_tipo() == nova_obra.obter_tipo()
            )
            if mesma_base and obra.dados_especificos() == nova_obra.dados_especificos():
                raise ValueError("Esta obra já está cadastrada no acervo.")

    @staticmethod
    def _copiar_para_biblioteca(origem: Path, pasta: Path, prefixo: str) -> Path:
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"{prefixo}_{origem.name}"
        if origem.resolve() != destino.resolve():
            shutil.copy2(origem, destino)
        return destino.resolve()

    @staticmethod
    def _excluir_arquivo_gerenciado(caminho: str, pasta_permitida: Path) -> None:
        arquivo = Path(caminho).resolve()
        try:
            arquivo.relative_to(pasta_permitida.resolve())
        except ValueError:
            return
        arquivo.unlink(missing_ok=True)


# Nome curto mantido para facilitar exemplos acadêmicos e imports antigos.
Biblioteca = BibliotecaDigital
