# BookReadNet

O **BookReadNet** é uma biblioteca digital desktop para organizar e ler HQs, mangás e livros. O sistema foi desenvolvido em Python para demonstrar, de forma prática, Programação Orientada a Objetos, modularização, persistência e interface gráfica com Tkinter.

## Funcionalidades

- Importação de arquivos `.pdf`, `.cbz`, `.cbr` e `.cb7`
- Cópia segura dos arquivos para a biblioteca gerenciada pelo sistema
- Cadastro, edição, pesquisa, filtros e exclusão de obras
- Classificação em HQ, Mangá ou Livro digital
- Metadados de autor, categoria, série, editora, idioma, volume ou edição
- Favoritos e status `Não iniciado`, `Em leitura` e `Lido`
- Leitor integrado com página anterior, próxima página e zoom
- Continuação automática da última página lida
- Histórico de leitura e porcentagem de progresso
- Persistência local em JSON

## Formatos

| Formato | Estrutura | Implementação |
|---|---|---|
| PDF | Documento paginado | PyMuPDF |
| CBZ | Imagens compactadas em ZIP | Biblioteca padrão `zipfile` |
| CBR | Imagens compactadas em RAR | `rarfile` |
| CB7 | Imagens compactadas em 7-Zip | `py7zr` |

> **Observação sobre CBR:** o pacote Python `rarfile` pode precisar de um programa compatível instalado no Windows, como 7-Zip, UnRAR ou bsdtar, principalmente para arquivos RAR comprimidos. PDF, CBZ e CB7 funcionam somente com as dependências do projeto.

## Conceitos de POO

- **Abstração:** `ObraDigital` e `LeitorArquivo` são classes abstratas.
- **Herança:** `HQ`, `Manga` e `LivroDigital` herdam de `ObraDigital`.
- **Polimorfismo:** `LeitorPDF`, `LeitorCBZ`, `LeitorCBR` e `LeitorCB7` implementam a mesma interface de leitura.
- **Encapsulamento:** os modelos usam atributos privados e propriedades para validar alterações.
- **Agregação:** `BibliotecaDigital` administra um conjunto de obras.
- **Composição:** o usuário local possui seus progressos e registros de histórico.
- **Associação:** o progresso relaciona o leitor a uma obra por seu identificador.

## Arquitetura

```text
main.py
  └── interface.py         Tkinter e interação com o usuário
        └── servicos.py    Regras do acervo e da leitura
              ├── modelos.py       Entidades e regras dos objetos
              ├── leitor.py        Leitores PDF/CBZ/CBR/CB7
              ├── persistencia.py  Repositório JSON
              └── validacoes.py    Arquivos e formatos aceitos
```

Arquivos gerados durante o uso:

```text
dados/bookreadnet.json
biblioteca/arquivos/
biblioteca/capas/
```

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m pip install -r requirements.txt
```

No Windows, também é possível usar:

```bat
run.bat
```

## Execução

```bash
python main.py
```

Na primeira execução, as pastas de dados e do acervo são criadas automaticamente.

## Testes

```bash
python -m pytest -v
```

Os testes cobrem cadastro, duplicidade, cópia de arquivos, pesquisa, filtros, favoritos, progresso, histórico, persistência, exclusão e leitura de CBZ.

## Como demonstrar

1. Abrir o BookReadNet e apresentar o painel do acervo.
2. Importar uma HQ ou mangá em PDF, CBZ, CBR ou CB7.
3. Mostrar os metadados e os filtros por tipo e status.
4. Favoritar a obra.
5. Abrir o leitor e avançar algumas páginas.
6. Fechar o leitor e mostrar a obra em `Continuar lendo`.
7. Abrir novamente e comprovar que a página foi restaurada.
8. Mostrar o histórico e o arquivo JSON salvo.
9. Explicar a fábrica de leitores como exemplo de polimorfismo.

## Fala curta para apresentação

> O BookReadNet começou como um sistema tradicional de biblioteca e evoluiu para uma biblioteca digital pessoal. A interface apenas recebe as ações do usuário; as regras ficam na classe BibliotecaDigital, os dados nas classes de modelo e cada formato possui seu próprio leitor. Com isso, conseguimos demonstrar abstração, herança, encapsulamento e polimorfismo em uma funcionalidade real: abrir uma obra, navegar pelas páginas e continuar depois exatamente de onde o usuário parou.

## Planejamento

O andamento das fases e as próximas evoluções estão em [ROADMAP.md](ROADMAP.md).
