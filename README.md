# BookReadNet

Sistema de biblioteca desenvolvido em Python com Programação Orientada a Objetos e interface gráfica Tkinter.

## Objetivo

Demonstrar, de forma prática, encapsulamento, herança, abstração, polimorfismo e relacionamento entre objetos.

## Funcionalidades

- Cadastrar livros
- Cadastrar usuários
- Listar registros
- Realizar empréstimos
- Realizar devoluções
- Excluir livros e usuários
- Validar dados de entrada

## Como executar

```bash
python main.py
```

## Estrutura

- `modelos.py`: classes de domínio
- `servicos.py`: regras de negócio da biblioteca
- `interface.py`: interface Tkinter
- `main.py`: inicialização e demonstração

## Conceitos de POO

- Encapsulamento com `@property`
- Herança entre `Pessoa`, `Usuario` e `Bibliotecario`
- Abstração com `abc`
- Polimorfismo via `exibir_dados()`
