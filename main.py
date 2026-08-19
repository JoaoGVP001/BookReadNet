from __future__ import annotations

import tkinter as tk

from interface import BibliotecaApp
from modelos import Bibliotecario, Livro, Usuario
from servicos import Biblioteca


def criar_biblioteca_exemplo() -> Biblioteca:
    biblioteca = Biblioteca("BookReadNet")

    biblioteca.cadastrar_bibliotecario(Bibliotecario("Admin", "admin@bookreadnet.com", "FUNC001"))
    biblioteca.cadastrar_usuario(Usuario("João", "joao@email.com", "U001"))
    biblioteca.cadastrar_usuario(Usuario("Maria", "maria@email.com", "U002"))
    biblioteca.cadastrar_livro(Livro("L001", "1984", "George Orwell", "Distopia"))
    biblioteca.cadastrar_livro(Livro("L002", "O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Clássico"))

    return biblioteca


def executar_demo_console(biblioteca: Biblioteca) -> None:
    print(f"Sistema: {biblioteca.nome}")
    print("Livros cadastrados:")
    for livro in biblioteca.listar_livros():
        print("-", livro)

    print("\nUsuários cadastrados:")
    for usuario in biblioteca.listar_usuarios():
        print("-", usuario)

    emprestimo = biblioteca.emprestar_livro("U001", "L001")
    print("\nEmpréstimo realizado:")
    print("-", emprestimo.exibir_dados())
    print("\nLivros após empréstimo:")
    for livro in biblioteca.listar_livros():
        print("-", livro)


def main() -> None:
    biblioteca = criar_biblioteca_exemplo()
    executar_demo_console(biblioteca)

    root = tk.Tk()
    BibliotecaApp(root, biblioteca)
    root.mainloop()


if __name__ == "__main__":
    main()
