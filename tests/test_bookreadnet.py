from __future__ import annotations

import base64
from pathlib import Path
from zipfile import ZipFile

import pytest

from leitor import FabricaLeitores, LeitorCB7, LeitorCBR, LeitorCBZ, LeitorPDF
from modelos import Manga, ProgressoLeitura, StatusLeitura
from servicos import BibliotecaDigital
from validacoes import FORMATOS_ACEITOS, validar_arquivo


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def criar_cbz(caminho: Path) -> Path:
    with ZipFile(caminho, "w") as arquivo:
        arquivo.writestr("pagina_10.png", PNG_1X1)
        arquivo.writestr("pagina_2.png", PNG_1X1)
        arquivo.writestr("notas.txt", "ignorar")
    return caminho


def criar_biblioteca(tmp_path: Path) -> BibliotecaDigital:
    return BibliotecaDigital("BookReadNet Teste", tmp_path)


def cadastrar_manga(biblioteca: BibliotecaDigital, arquivo: Path, titulo: str = "Berserk") -> Manga:
    obra = biblioteca.cadastrar_obra(
        tipo="Mangá",
        titulo=titulo,
        autor="Kentaro Miura",
        caminho_arquivo=str(arquivo),
        categoria="Fantasia",
        serie="Berserk",
        volume="1",
    )
    assert isinstance(obra, Manga)
    return obra


def test_formatos_principais_estao_habilitados() -> None:
    assert set(FORMATOS_ACEITOS) == {".pdf", ".cbz", ".cbr", ".cb7"}


def test_validacao_rejeita_arquivo_inexistente(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="não existe"):
        validar_arquivo(tmp_path / "inexistente.cbz")


def test_cadastro_copia_arquivo_e_persiste_acervo(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "berserk.cbz")
    biblioteca = criar_biblioteca(tmp_path)

    obra = cadastrar_manga(biblioteca, origem)
    recarregada = criar_biblioteca(tmp_path)

    assert Path(obra.caminho_arquivo).exists()
    assert Path(obra.caminho_arquivo).parent.name == "arquivos"
    assert len(recarregada.obras) == 1
    assert recarregada.obras[0].titulo == "Berserk"
    assert recarregada.obras[0].serie == "Berserk"


def test_impede_cadastro_duplicado_e_remove_copia_criada(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "berserk.cbz")
    biblioteca = criar_biblioteca(tmp_path)
    cadastrar_manga(biblioteca, origem)

    with pytest.raises(ValueError, match="já está cadastrada"):
        cadastrar_manga(biblioteca, origem)

    assert len(list(biblioteca.pasta_arquivos.glob("*.cbz"))) == 1


def test_favoritos_busca_e_filtros(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "berserk.cbz")
    biblioteca = criar_biblioteca(tmp_path)
    obra = cadastrar_manga(biblioteca, origem)

    assert biblioteca.pesquisar("miura") == [obra]
    assert biblioteca.filtrar(tipo="HQ") == []
    assert biblioteca.alternar_favorito(obra.id_obra) is True
    assert biblioteca.filtrar(somente_favoritos=True) == [obra]


def test_progresso_valida_paginas_e_altera_status() -> None:
    progresso = ProgressoLeitura("OBRA1")
    progresso.atualizar_pagina(2, 10)
    assert progresso.porcentagem == 20.0
    assert progresso.status == StatusLeitura.EM_LEITURA

    progresso.atualizar_pagina(10, 10)
    assert progresso.status == StatusLeitura.LIDO

    with pytest.raises(ValueError, match="ultrapassar"):
        progresso.atualizar_pagina(11, 10)


def test_servico_salva_progresso_e_historico(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "berserk.cbz")
    biblioteca = criar_biblioteca(tmp_path)
    obra = cadastrar_manga(biblioteca, origem)

    progresso = biblioteca.salvar_progresso(obra.id_obra, 2, 2)
    recarregada = criar_biblioteca(tmp_path)

    assert progresso.status == StatusLeitura.LIDO
    assert obra.status_leitura == StatusLeitura.LIDO
    assert recarregada.obter_progresso(obra.id_obra).pagina_atual == 2
    assert "Berserk" in recarregada.listar_historico()[0]


def test_leitor_cbz_ordena_paginas_naturalmente(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "quadrinho.cbz")
    leitor = FabricaLeitores.criar(origem)

    assert isinstance(leitor, LeitorCBZ)
    assert leitor.total_paginas == 2
    assert leitor._paginas == ["pagina_2.png", "pagina_10.png"]
    assert leitor.obter_pagina(0).size == (1, 1)
    leitor.fechar()


def test_leitor_pdf_renderiza_pagina(tmp_path: Path) -> None:
    import fitz

    caminho = tmp_path / "quadrinho.pdf"
    documento = fitz.open()
    pagina = documento.new_page(width=300, height=400)
    pagina.insert_text((40, 60), "BookReadNet")
    documento.save(caminho)
    documento.close()

    leitor = FabricaLeitores.criar(caminho)

    assert isinstance(leitor, LeitorPDF)
    assert leitor.total_paginas == 1
    assert leitor.obter_pagina(0).width > 300
    leitor.fechar()


def test_leitor_cb7_extrai_imagens(tmp_path: Path) -> None:
    import py7zr

    imagem = tmp_path / "pagina_1.png"
    imagem.write_bytes(PNG_1X1)
    caminho = tmp_path / "quadrinho.cb7"
    with py7zr.SevenZipFile(caminho, "w") as arquivo:
        arquivo.write(imagem, arcname="pagina_1.png")

    leitor = FabricaLeitores.criar(caminho)

    assert isinstance(leitor, LeitorCB7)
    assert leitor.total_paginas == 1
    assert leitor.obter_pagina(0).size == (1, 1)
    leitor.fechar()


def test_fabrica_direciona_cbr_ao_leitor_rar(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    caminho = tmp_path / "quadrinho.cbr"
    caminho.write_bytes(b"RAR de teste")
    monkeypatch.setattr(LeitorCBR, "abrir", lambda self: setattr(self, "_aberto", True))

    leitor = FabricaLeitores.criar(caminho)

    assert isinstance(leitor, LeitorCBR)
    leitor.fechar()


def test_exclusao_remove_progresso_e_arquivo_quando_confirmado(tmp_path: Path) -> None:
    origem = criar_cbz(tmp_path / "berserk.cbz")
    biblioteca = criar_biblioteca(tmp_path)
    obra = cadastrar_manga(biblioteca, origem)
    arquivo_copiado = Path(obra.caminho_arquivo)
    biblioteca.salvar_progresso(obra.id_obra, 1, 2)

    biblioteca.excluir_obra(obra.id_obra, excluir_arquivo=True)

    assert biblioteca.obras == []
    assert not arquivo_copiado.exists()
    assert obra.id_obra not in biblioteca.usuario.progressos
