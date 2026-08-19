# BookReadNet

BookReadNet é um sistema de biblioteca em Python criado para a disciplina de Programação Orientada a Objetos 1. O projeto mostra, na prática, como usar encapsulamento, herança, abstração, polimorfismo e relações entre objetos em um sistema funcional com Tkinter.

## Resumo rápido para apresentação

> O BookReadNet é um sistema de biblioteca desenvolvido em Python com foco em POO. Ele permite cadastrar livros e usuários, controlar empréstimos e devoluções, aplicar validações e exibir tudo em uma interface gráfica simples.

## O que o sistema faz

- Cadastra livros
- Cadastra usuários
- Lista livros, usuários e empréstimos
- Realiza empréstimos
- Realiza devoluções
- Exclui livros e usuários
- Valida dados de entrada
- Exibe mensagens de sucesso e erro na interface

## Conceitos de POO aplicados

- Encapsulamento com atributos privados e `@property`
- Herança entre `Pessoa`, `Usuario` e `Bibliotecario`
- Abstração com `abc` e `@abstractmethod`
- Polimorfismo no método `exibir_dados()`
- Associação entre usuário, livro e empréstimo
- Agregação da biblioteca com seus registros

## Estrutura do projeto

- `modelos.py`: classes de domínio
- `servicos.py`: regras de negócio da biblioteca
- `interface.py`: interface gráfica Tkinter
- `main.py`: ponto de entrada e demonstração inicial
- `tests/`: testes automatizados das regras principais
- `run.bat`: atalho para abrir o sistema no Windows

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

Ou, no Windows:

```bash
run.bat
```

### Testes

```bash
pytest
```

## Roteiro de demonstração oral

1. Apresentar o nome do sistema e o objetivo do projeto
2. Explicar rapidamente a divisão dos arquivos
3. Mostrar as classes principais e os conceitos de POO usados
4. Abrir a interface e cadastrar um livro
5. Cadastrar um usuário
6. Realizar um empréstimo
7. Mostrar que o livro fica indisponível
8. Tentar emprestar o mesmo livro novamente para mostrar a validação
9. Fazer a devolução
10. Mostrar o livro disponível novamente

## Texto curto para a fala do grupo

> O nosso sistema, BookReadNet, foi desenvolvido para organizar o fluxo básico de uma biblioteca. Primeiro modelamos as entidades com POO, depois centralizamos as regras de negócio em uma classe de serviço e por fim criamos a interface gráfica com Tkinter. Assim, a interface apenas chama os métodos do sistema, enquanto a lógica fica separada e organizada.

## Pontos para destacar na apresentação

- A interface não contém regra de negócio
- As validações estão concentradas na camada de serviço e nos modelos
- Os testes confirmam os fluxos principais do sistema
- O projeto foi estruturado para ser simples de explicar e demonstrar

## Sugestão de ordem de fala

- Pessoa 1: objetivo e estrutura do projeto
- Pessoa 2: classes e POO
- Pessoa 3: regras de negócio e testes
- Pessoa 4: interface e demonstração final
