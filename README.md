# BookReadNet

BookReadNet é um sistema de biblioteca desenvolvido em Python para a disciplina de Programação Orientada a Objetos 1. O projeto demonstra, na prática, conceitos de encapsulamento, herança, abstração, polimorfismo e relacionamentos entre objetos, com interface gráfica simples em Tkinter.

## Sobre o projeto

O sistema permite cadastrar livros e usuários, realizar empréstimos e devoluções, excluir registros e visualizar a situação dos itens cadastrados.

## Funcionalidades implementadas

- Cadastro de livros
- Cadastro de usuários
- Listagem de livros, usuários e empréstimos
- Empréstimo de livros
- Devolução de livros
- Exclusão de livros e usuários
- Validações de entrada e regras de negócio
- Interface gráfica com Tkinter

## Conceitos de POO aplicados

- Encapsulamento com atributos privados e `@property`
- Herança entre `Pessoa`, `Usuario` e `Bibliotecario`
- Abstração com `abc` e `@abstractmethod`
- Polimorfismo no método `exibir_dados()`
- Associação entre usuário, livro e empréstimo
- Agregação da biblioteca com seus registros

## Estrutura do projeto

- `modelos.py`: classes de domínio
- `servicos.py`: regras de negócio do sistema
- `interface.py`: interface gráfica Tkinter
- `main.py`: ponto de entrada da aplicação
- `tests/`: testes automatizados das regras principais

## Como executar

### Requisitos

- Python 3.10 ou superior

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

### Testes

```bash
pytest
```

## Roteiro de demonstração

1. Abrir o sistema
2. Cadastrar um livro
3. Cadastrar um usuário
4. Realizar um empréstimo
5. Mostrar o livro como indisponível
6. Tentar emprestar novamente para exibir a validação
7. Realizar a devolução
8. Mostrar o livro como disponível novamente

## Observações para apresentação

- O código da interface apenas chama os métodos das classes de serviço
- As regras de negócio ficam centralizadas em `servicos.py`
- Os testes cobrem os fluxos principais do sistema
