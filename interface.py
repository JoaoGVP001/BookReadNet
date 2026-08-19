from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from modelos import Livro, Usuario
from servicos import Biblioteca


class BibliotecaApp:
    def __init__(self, root: tk.Tk, biblioteca: Biblioteca) -> None:
        self.root = root
        self.biblioteca = biblioteca
        self.root.title("BookReadNet")
        self.root.geometry("980x650")
        self.root.minsize(900, 600)

        estilo = ttk.Style()
        estilo.theme_use("clam")

        cabecalho = ttk.Frame(root, padding=(18, 16))
        cabecalho.pack(fill="x")
        ttk.Label(cabecalho, text="BookReadNet", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            cabecalho,
            text="Sistema de biblioteca em Python com POO e Tkinter",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self._build_livros_tab()
        self._build_usuarios_tab()
        self._build_emprestimos_tab()

    def _build_livros_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Livros")

        self.livro_id = tk.StringVar()
        self.livro_titulo = tk.StringVar()
        self.livro_autor = tk.StringVar()
        self.livro_categoria = tk.StringVar()

        campos = [
            ("ID", self.livro_id),
            ("Título", self.livro_titulo),
            ("Autor", self.livro_autor),
            ("Categoria", self.livro_categoria),
        ]
        for i, (rotulo, var) in enumerate(campos):
            ttk.Label(frame, text=rotulo).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(frame, textvariable=var, width=35).grid(row=i, column=1, sticky="w", pady=4)

        ttk.Button(frame, text="Cadastrar livro", command=self.cadastrar_livro).grid(row=4, column=0, pady=8)
        ttk.Button(frame, text="Excluir livro", command=self.excluir_livro).grid(row=4, column=1, pady=8, sticky="w")
        ttk.Button(frame, text="Atualizar lista", command=self.atualizar_livros).grid(row=4, column=2, pady=8, sticky="w")
        ttk.Button(frame, text="Limpar campos", command=self.limpar_campos_livro).grid(row=4, column=3, pady=8, sticky="w")

        self.lista_livros = tk.Listbox(frame, width=110, height=18)
        self.lista_livros.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)

    def _build_usuarios_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Usuários")

        self.usuario_nome = tk.StringVar()
        self.usuario_email = tk.StringVar()
        self.usuario_matricula = tk.StringVar()

        campos = [
            ("Nome", self.usuario_nome),
            ("E-mail", self.usuario_email),
            ("Matrícula", self.usuario_matricula),
        ]
        for i, (rotulo, var) in enumerate(campos):
            ttk.Label(frame, text=rotulo).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(frame, textvariable=var, width=35).grid(row=i, column=1, sticky="w", pady=4)

        ttk.Button(frame, text="Cadastrar usuário", command=self.cadastrar_usuario).grid(row=3, column=0, pady=8)
        ttk.Button(frame, text="Excluir usuário", command=self.excluir_usuario).grid(row=3, column=1, pady=8, sticky="w")
        ttk.Button(frame, text="Atualizar lista", command=self.atualizar_usuarios).grid(row=3, column=2, pady=8, sticky="w")
        ttk.Button(frame, text="Limpar campos", command=self.limpar_campos_usuario).grid(row=3, column=3, pady=8, sticky="w")

        self.lista_usuarios = tk.Listbox(frame, width=110, height=18)
        self.lista_usuarios.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)

    def _build_emprestimos_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Empréstimos")

        self.emprestimo_matricula = tk.StringVar()
        self.emprestimo_livro_id = tk.StringVar()

        ttk.Label(frame, text="Matrícula do usuário").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.emprestimo_matricula, width=35).grid(row=0, column=1, sticky="w", pady=4)
        ttk.Label(frame, text="ID do livro").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.emprestimo_livro_id, width=35).grid(row=1, column=1, sticky="w", pady=4)

        ttk.Button(frame, text="Emprestar", command=self.realizar_emprestimo).grid(row=2, column=0, pady=8)
        ttk.Button(frame, text="Devolver", command=self.realizar_devolucao).grid(row=2, column=1, pady=8, sticky="w")
        ttk.Button(frame, text="Atualizar lista", command=self.atualizar_emprestimos).grid(row=2, column=2, pady=8, sticky="w")
        ttk.Button(frame, text="Limpar campos", command=self.limpar_campos_emprestimo).grid(row=2, column=3, pady=8, sticky="w")

        self.lista_emprestimos = tk.Listbox(frame, width=110, height=18)
        self.lista_emprestimos.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)

    def cadastrar_livro(self) -> None:
        try:
            livro = Livro(
                self.livro_id.get(),
                self.livro_titulo.get(),
                self.livro_autor.get(),
                self.livro_categoria.get(),
            )
            self.biblioteca.cadastrar_livro(livro)
            self.atualizar_livros()
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_livro(self) -> None:
        try:
            self.biblioteca.remover_livro(self.livro_id.get())
            self.atualizar_livros()
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def cadastrar_usuario(self) -> None:
        try:
            usuario = Usuario(self.usuario_nome.get(), self.usuario_email.get(), self.usuario_matricula.get())
            self.biblioteca.cadastrar_usuario(usuario)
            self.atualizar_usuarios()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_usuario(self) -> None:
        try:
            self.biblioteca.remover_usuario(self.usuario_matricula.get())
            self.atualizar_usuarios()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def realizar_emprestimo(self) -> None:
        try:
            self.biblioteca.emprestar_livro(self.emprestimo_matricula.get(), self.emprestimo_livro_id.get())
            self.atualizar_tudo()
            messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def realizar_devolucao(self) -> None:
        try:
            self.biblioteca.devolver_livro(self.emprestimo_matricula.get(), self.emprestimo_livro_id.get())
            self.atualizar_tudo()
            messagebox.showinfo("Sucesso", "Devolução realizada com sucesso.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def atualizar_livros(self) -> None:
        self.lista_livros.delete(0, tk.END)
        for item in self.biblioteca.listar_livros():
            self.lista_livros.insert(tk.END, item)

    def atualizar_usuarios(self) -> None:
        self.lista_usuarios.delete(0, tk.END)
        for item in self.biblioteca.listar_usuarios():
            self.lista_usuarios.insert(tk.END, item)

    def atualizar_emprestimos(self) -> None:
        self.lista_emprestimos.delete(0, tk.END)
        for item in self.biblioteca.listar_emprestimos():
            self.lista_emprestimos.insert(tk.END, item)

    def atualizar_tudo(self) -> None:
        self.atualizar_livros()
        self.atualizar_usuarios()
        self.atualizar_emprestimos()

    def limpar_campos_livro(self) -> None:
        self.livro_id.set("")
        self.livro_titulo.set("")
        self.livro_autor.set("")
        self.livro_categoria.set("")

    def limpar_campos_usuario(self) -> None:
        self.usuario_nome.set("")
        self.usuario_email.set("")
        self.usuario_matricula.set("")

    def limpar_campos_emprestimo(self) -> None:
        self.emprestimo_matricula.set("")
        self.emprestimo_livro_id.set("")
