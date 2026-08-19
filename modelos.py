from __future__ import annotations

from abc import ABC, abstractmethod


class Pessoa(ABC):
    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome não pode estar vazio.")
        self.__nome = valor

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O e-mail não pode estar vazio.")
        self.__email = valor

    @abstractmethod
    def exibir_dados(self) -> str:
        raise NotImplementedError


class Usuario(Pessoa):
    def __init__(self, nome: str, email: str, matricula: str) -> None:
        super().__init__(nome, email)
        self.matricula = matricula
        self.__livros_emprestados: list[Livro] = []

    @property
    def matricula(self) -> str:
        return self.__matricula

    @matricula.setter
    def matricula(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("A matrícula não pode estar vazia.")
        self.__matricula = valor

    @property
    def livros_emprestados(self) -> list[Livro]:
        return list(self.__livros_emprestados)

    def adicionar_livro(self, livro: Livro) -> None:
        self.__livros_emprestados.append(livro)

    def remover_livro(self, livro: Livro) -> None:
        if livro in self.__livros_emprestados:
            self.__livros_emprestados.remove(livro)

    def exibir_dados(self) -> str:
        return f"Usuário: {self.nome} | E-mail: {self.email} | Matrícula: {self.matricula}"


class Bibliotecario(Pessoa):
    def __init__(self, nome: str, email: str, codigo_funcionario: str) -> None:
        super().__init__(nome, email)
        self.codigo_funcionario = codigo_funcionario

    @property
    def codigo_funcionario(self) -> str:
        return self.__codigo_funcionario

    @codigo_funcionario.setter
    def codigo_funcionario(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O código do funcionário não pode estar vazio.")
        self.__codigo_funcionario = valor

    def exibir_dados(self) -> str:
        return f"Bibliotecário: {self.nome} | E-mail: {self.email} | Código: {self.codigo_funcionario}"


class Livro:
    def __init__(self, id_livro: str, titulo: str, autor: str, categoria: str) -> None:
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.__disponivel = True

    @property
    def id_livro(self) -> str:
        return self.__id_livro

    @id_livro.setter
    def id_livro(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O ID do livro não pode estar vazio.")
        self.__id_livro = valor

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O título não pode estar vazio.")
        self.__titulo = valor

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O autor não pode estar vazio.")
        self.__autor = valor

    @property
    def categoria(self) -> str:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("A categoria não pode estar vazia.")
        self.__categoria = valor

    @property
    def disponivel(self) -> bool:
        return self.__disponivel

    def emprestar(self) -> None:
        self.__disponivel = False

    def devolver(self) -> None:
        self.__disponivel = True

    def exibir_dados(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} | {self.autor} | {self.categoria} | {status}"


class Emprestimo:
    def __init__(self, usuario: Usuario, livro: Livro, data_emprestimo: str) -> None:
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao: str | None = None

    def registrar_devolucao(self, data_devolucao: str) -> None:
        self.data_devolucao = data_devolucao

    def exibir_dados(self) -> str:
        devolucao = self.data_devolucao or "Pendente"
        return f"{self.usuario.nome} -> {self.livro.titulo} | Empréstimo: {self.data_emprestimo} | Devolução: {devolucao}"
