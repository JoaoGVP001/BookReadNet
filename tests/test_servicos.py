from servicos import Biblioteca
from modelos import Livro, Usuario, Bibliotecario


def criar_biblioteca() -> Biblioteca:
    biblioteca = Biblioteca("BookReadNet")
    biblioteca.cadastrar_bibliotecario(Bibliotecario("Admin", "admin@bookreadnet.com", "FUNC001"))
    biblioteca.cadastrar_usuario(Usuario("João", "joao@email.com", "U001"))
    biblioteca.cadastrar_livro(Livro("L001", "1984", "George Orwell", "Distopia"))
    return biblioteca


def test_cadastrar_livro_e_listar():
    biblioteca = criar_biblioteca()

    livros = biblioteca.listar_livros()

    assert len(livros) == 1
    assert "1984" in livros[0]


def test_impede_livro_com_id_duplicado():
    biblioteca = criar_biblioteca()

    try:
        biblioteca.cadastrar_livro(Livro("L001", "Animal Farm", "George Orwell", "Distopia"))
    except ValueError as erro:
        assert "ID" in str(erro)
    else:
        raise AssertionError("Era esperado erro de ID duplicado.")


def test_emprestimo_altera_disponibilidade():
    biblioteca = criar_biblioteca()

    emprestimo = biblioteca.emprestar_livro("U001", "L001")

    assert emprestimo.livro.disponivel is False
    assert "Emprestado" in biblioteca.listar_livros()[0]


def test_impede_segundo_emprestimo_mesmo_livro():
    biblioteca = criar_biblioteca()
    biblioteca.emprestar_livro("U001", "L001")

    try:
        biblioteca.emprestar_livro("U001", "L001")
    except ValueError as erro:
        assert "indisponível" in str(erro)
    else:
        raise AssertionError("Era esperado erro de livro indisponível.")


def test_devolucao_retorna_disponibilidade():
    biblioteca = criar_biblioteca()
    biblioteca.emprestar_livro("U001", "L001")

    biblioteca.devolver_livro("U001", "L001")

    assert "Disponível" in biblioteca.listar_livros()[0]
