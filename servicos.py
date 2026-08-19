from __future__ import annotations

from datetime import date

from modelos import Bibliotecario, Emprestimo, Livro, Usuario


class Biblioteca:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.__livros: list[Livro] = []
        self.__usuarios: list[Usuario] = []
        self.__bibliotecarios: list[Bibliotecario] = []
        self.__emprestimos: list[Emprestimo] = []

    @property
    def livros(self) -> list[Livro]:
        return list(self.__livros)

    @property
    def usuarios(self) -> list[Usuario]:
        return list(self.__usuarios)

    @property
    def emprestimos(self) -> list[Emprestimo]:
        return list(self.__emprestimos)

    def cadastrar_livro(self, livro: Livro) -> None:
        if any(item.id_livro == livro.id_livro for item in self.__livros):
            raise ValueError("Já existe um livro com esse ID.")
        self.__livros.append(livro)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        if any(item.matricula == usuario.matricula for item in self.__usuarios):
            raise ValueError("Já existe um usuário com essa matrícula.")
        self.__usuarios.append(usuario)

    def cadastrar_bibliotecario(self, bibliotecario: Bibliotecario) -> None:
        self.__bibliotecarios.append(bibliotecario)

    def buscar_livro_por_id(self, id_livro: str) -> Livro:
        for livro in self.__livros:
            if livro.id_livro == id_livro:
                return livro
        raise ValueError("Livro não encontrado.")

    def buscar_usuario_por_matricula(self, matricula: str) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.matricula == matricula:
                return usuario
        raise ValueError("Usuário não encontrado.")

    def remover_livro(self, id_livro: str) -> None:
        livro = self.buscar_livro_por_id(id_livro)
        if not livro.disponivel:
            raise ValueError("Não é possível excluir um livro emprestado.")
        self.__livros.remove(livro)

    def remover_usuario(self, matricula: str) -> None:
        usuario = self.buscar_usuario_por_matricula(matricula)
        if usuario.livros_emprestados:
            raise ValueError("Não é possível excluir usuário com livros emprestados.")
        self.__usuarios.remove(usuario)

    def emprestar_livro(self, matricula: str, id_livro: str) -> Emprestimo:
        usuario = self.buscar_usuario_por_matricula(matricula)
        livro = self.buscar_livro_por_id(id_livro)
        if not livro.disponivel:
            raise ValueError("Livro indisponível.")
        livro.emprestar()
        usuario.adicionar_livro(livro)
        emprestimo = Emprestimo(usuario, livro, str(date.today()))
        self.__emprestimos.append(emprestimo)
        return emprestimo

    def devolver_livro(self, matricula: str, id_livro: str) -> Emprestimo:
        usuario = self.buscar_usuario_por_matricula(matricula)
        livro = self.buscar_livro_por_id(id_livro)
        for emprestimo in self.__emprestimos:
            if emprestimo.usuario == usuario and emprestimo.livro == livro and emprestimo.data_devolucao is None:
                livro.devolver()
                usuario.remover_livro(livro)
                emprestimo.registrar_devolucao(str(date.today()))
                return emprestimo
        raise ValueError("Empréstimo não encontrado para devolução.")

    def listar_livros(self) -> list[str]:
        return [livro.exibir_dados() for livro in self.__livros]

    def listar_usuarios(self) -> list[str]:
        return [usuario.exibir_dados() for usuario in self.__usuarios]

    def listar_emprestimos(self) -> list[str]:
        return [emprestimo.exibir_dados() for emprestimo in self.__emprestimos]
