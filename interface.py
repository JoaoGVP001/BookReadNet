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
        self.root.geometry("1040x720")
        self.root.minsize(940, 640)
        self.root.configure(bg="#f4f1ea")

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f4f1ea")
        estilo.configure("Header.TFrame", background="#1f2937")
        estilo.configure("Header.TLabel", background="#1f2937", foreground="#f9fafb")
        estilo.configure("SubHeader.TLabel", background="#1f2937", foreground="#d1d5db")
        estilo.configure("Card.TFrame", background="#ffffff")
        estilo.configure("Title.TLabel", background="#f4f1ea", foreground="#111827", font=("Segoe UI", 18, "bold"))
        estilo.configure("Section.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 11, "bold"))
        estilo.configure("TLabel", background="#f4f1ea", foreground="#111827", font=("Segoe UI", 10))
        estilo.configure("TButton", padding=(12, 6), font=("Segoe UI", 10, "bold"))
        estilo.configure("TNotebook", background="#f4f1ea", borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10, "bold"))

        cabecalho = ttk.Frame(root, style="Header.TFrame", padding=(20, 18))
        cabecalho.pack(fill="x")
        ttk.Label(cabecalho, text="BookReadNet", style="Header.TLabel", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            cabecalho,
            text="Sistema de biblioteca em Python com POO e Tkinter",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        conteudo = ttk.Frame(root, padding=16)
        conteudo.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(conteudo)
        self.notebook.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="Pronto para usar.")
        status = ttk.Label(root, textvariable=self.status_var, anchor="w", padding=(16, 8))
        status.pack(fill="x")

        self._build_livros_tab()
        self._build_usuarios_tab()
        self._build_emprestimos_tab()

    def _build_livros_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        self.notebook.add(frame, text="Livros")

        self.livro_id = tk.StringVar()
        self.livro_titulo = tk.StringVar()
        self.livro_autor = tk.StringVar()
        self.livro_categoria = tk.StringVar()

        ttk.Label(frame, text="Cadastro de livros", style="Section.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 14))

        campos = [
            ("ID", self.livro_id),
            ("Título", self.livro_titulo),
            ("Autor", self.livro_autor),
            ("Categoria", self.livro_categoria),
        ]
        for i, (rotulo, var) in enumerate(campos, start=1):
            ttk.Label(frame, text=rotulo).grid(row=i, column=0, sticky="w", pady=6, padx=(0, 10))
            ttk.Entry(frame, textvariable=var, width=42).grid(row=i, column=1, sticky="w", pady=6)

        botoes = ttk.Frame(frame, style="Card.TFrame")
        botoes.grid(row=5, column=0, columnspan=4, sticky="w", pady=(14, 10))
        ttk.Button(botoes, text="Cadastrar livro", command=self.cadastrar_livro).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Excluir livro", command=self.excluir_livro).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar lista", command=self.atualizar_livros).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(botoes, text="Limpar campos", command=self.limpar_campos_livro).grid(row=0, column=3)

        self.lista_livros = tk.Listbox(frame, width=110, height=18, relief="flat", borderwidth=0, highlightthickness=1, highlightbackground="#d1d5db")
        self.lista_livros.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=8)
        scrollbar_livros = ttk.Scrollbar(frame, orient="vertical", command=self.lista_livros.yview)
        scrollbar_livros.grid(row=6, column=4, sticky="ns")
        self.lista_livros.configure(yscrollcommand=scrollbar_livros.set)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(6, weight=1)

    def _build_usuarios_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        self.notebook.add(frame, text="Usuários")

        self.usuario_nome = tk.StringVar()
        self.usuario_email = tk.StringVar()
        self.usuario_matricula = tk.StringVar()

        ttk.Label(frame, text="Cadastro de usuários", style="Section.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 14))

        campos = [
            ("Nome", self.usuario_nome),
            ("E-mail", self.usuario_email),
            ("Matrícula", self.usuario_matricula),
        ]
        for i, (rotulo, var) in enumerate(campos, start=1):
            ttk.Label(frame, text=rotulo).grid(row=i, column=0, sticky="w", pady=6, padx=(0, 10))
            ttk.Entry(frame, textvariable=var, width=42).grid(row=i, column=1, sticky="w", pady=6)

        botoes = ttk.Frame(frame, style="Card.TFrame")
        botoes.grid(row=4, column=0, columnspan=4, sticky="w", pady=(14, 10))
        ttk.Button(botoes, text="Cadastrar usuário", command=self.cadastrar_usuario).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Excluir usuário", command=self.excluir_usuario).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar lista", command=self.atualizar_usuarios).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(botoes, text="Limpar campos", command=self.limpar_campos_usuario).grid(row=0, column=3)

        self.lista_usuarios = tk.Listbox(frame, width=110, height=18, relief="flat", borderwidth=0, highlightthickness=1, highlightbackground="#d1d5db")
        self.lista_usuarios.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=8)
        scrollbar_usuarios = ttk.Scrollbar(frame, orient="vertical", command=self.lista_usuarios.yview)
        scrollbar_usuarios.grid(row=5, column=4, sticky="ns")
        self.lista_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

    def _build_emprestimos_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        self.notebook.add(frame, text="Empréstimos")

        self.emprestimo_matricula = tk.StringVar()
        self.emprestimo_livro_id = tk.StringVar()

        ttk.Label(frame, text="Controle de empréstimos", style="Section.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 14))

        ttk.Label(frame, text="Matrícula do usuário").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        ttk.Entry(frame, textvariable=self.emprestimo_matricula, width=42).grid(row=1, column=1, sticky="w", pady=6)
        ttk.Label(frame, text="ID do livro").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        ttk.Entry(frame, textvariable=self.emprestimo_livro_id, width=42).grid(row=2, column=1, sticky="w", pady=6)

        botoes = ttk.Frame(frame, style="Card.TFrame")
        botoes.grid(row=3, column=0, columnspan=4, sticky="w", pady=(14, 10))
        ttk.Button(botoes, text="Emprestar", command=self.realizar_emprestimo).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Devolver", command=self.realizar_devolucao).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar lista", command=self.atualizar_emprestimos).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(botoes, text="Limpar campos", command=self.limpar_campos_emprestimo).grid(row=0, column=3)

        self.lista_emprestimos = tk.Listbox(frame, width=110, height=18, relief="flat", borderwidth=0, highlightthickness=1, highlightbackground="#d1d5db")
        self.lista_emprestimos.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=8)
        scrollbar_emprestimos = ttk.Scrollbar(frame, orient="vertical", command=self.lista_emprestimos.yview)
        scrollbar_emprestimos.grid(row=4, column=4, sticky="ns")
        self.lista_emprestimos.configure(yscrollcommand=scrollbar_emprestimos.set)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(4, weight=1)

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
            self.status_var.set("Livro cadastrado com sucesso.")
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso.")
            self.limpar_campos_livro()
        except ValueError as erro:
            self.status_var.set("Falha ao cadastrar livro.")
            messagebox.showerror("Erro", str(erro))

    def excluir_livro(self) -> None:
        try:
            self.biblioteca.remover_livro(self.livro_id.get())
            self.atualizar_livros()
            self.status_var.set("Livro excluído com sucesso.")
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso.")
            self.limpar_campos_livro()
        except ValueError as erro:
            self.status_var.set("Falha ao excluir livro.")
            messagebox.showerror("Erro", str(erro))

    def cadastrar_usuario(self) -> None:
        try:
            usuario = Usuario(self.usuario_nome.get(), self.usuario_email.get(), self.usuario_matricula.get())
            self.biblioteca.cadastrar_usuario(usuario)
            self.atualizar_usuarios()
            self.status_var.set("Usuário cadastrado com sucesso.")
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
            self.limpar_campos_usuario()
        except ValueError as erro:
            self.status_var.set("Falha ao cadastrar usuário.")
            messagebox.showerror("Erro", str(erro))

    def excluir_usuario(self) -> None:
        try:
            self.biblioteca.remover_usuario(self.usuario_matricula.get())
            self.atualizar_usuarios()
            self.status_var.set("Usuário excluído com sucesso.")
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
            self.limpar_campos_usuario()
        except ValueError as erro:
            self.status_var.set("Falha ao excluir usuário.")
            messagebox.showerror("Erro", str(erro))

    def realizar_emprestimo(self) -> None:
        try:
            self.biblioteca.emprestar_livro(self.emprestimo_matricula.get(), self.emprestimo_livro_id.get())
            self.atualizar_tudo()
            self.status_var.set("Empréstimo realizado com sucesso.")
            messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso.")
            self.limpar_campos_emprestimo()
        except ValueError as erro:
            self.status_var.set("Falha ao realizar empréstimo.")
            messagebox.showerror("Erro", str(erro))

    def realizar_devolucao(self) -> None:
        try:
            self.biblioteca.devolver_livro(self.emprestimo_matricula.get(), self.emprestimo_livro_id.get())
            self.atualizar_tudo()
            self.status_var.set("Devolução realizada com sucesso.")
            messagebox.showinfo("Sucesso", "Devolução realizada com sucesso.")
            self.limpar_campos_emprestimo()
        except ValueError as erro:
            self.status_var.set("Falha ao realizar devolução.")
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
