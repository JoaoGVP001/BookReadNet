# BookReadNet - Roadmap da Biblioteca Digital

Este roadmap acompanha a evolução do sistema acadêmico de biblioteca para um gerenciador e leitor pessoal de HQs, mangás e livros digitais.

<details open>
<summary><strong>1. Modelagem orientada a objetos - concluída</strong></summary>

- [x] Classe abstrata `ObraDigital`
- [x] Especializações `HQ`, `Manga` e `LivroDigital`
- [x] Classes `Categoria`, `Serie`, `Usuario`, `ProgressoLeitura` e `HistoricoLeitura`
- [x] Encapsulamento com propriedades e validações
- [x] Status de leitura separado de favorito

</details>

<details open>
<summary><strong>2. Acervo e regras de negócio - concluída</strong></summary>

- [x] Cadastrar, editar, excluir, listar e pesquisar obras
- [x] Filtrar por tipo, status e favorito
- [x] Impedir obra duplicada
- [x] Remover progresso ao excluir uma obra
- [x] Separar as regras da interface Tkinter

</details>

<details open>
<summary><strong>3. Upload e organização de arquivos - concluída</strong></summary>

- [x] Seleção de arquivo com `filedialog`
- [x] Formatos aceitos: PDF, CBZ, CBR e CB7
- [x] Validação de existência, extensão e tamanho
- [x] Cópia para `biblioteca/arquivos`
- [x] Capas opcionais em `biblioteca/capas`
- [x] Confirmação separada antes de remover o arquivo físico

</details>

<details open>
<summary><strong>4. Arquitetura polimórfica de leitura - concluída</strong></summary>

- [x] Classe abstrata `LeitorArquivo`
- [x] `LeitorPDF` com PyMuPDF
- [x] `LeitorCBZ` com ZIP
- [x] `LeitorCBR` com RAR
- [x] `LeitorCB7` com 7-Zip
- [x] `FabricaLeitores` para selecionar a implementação pelo formato
- [x] Ordenação natural das imagens (`2` antes de `10`)

</details>

<details open>
<summary><strong>5. Progresso e persistência - concluída</strong></summary>

- [x] Página atual e total de páginas
- [x] Cálculo de porcentagem
- [x] Atualização automática do status
- [x] Histórico das últimas leituras
- [x] Tela `Continuar lendo`
- [x] Persistência local em JSON
- [x] Gravação atômica para reduzir risco de arquivo incompleto

</details>

<details open>
<summary><strong>6. Interface Tkinter - concluída</strong></summary>

- [x] Navegação lateral
- [x] Painel com métricas do acervo
- [x] Cadastro e edição de metadados
- [x] Pesquisa, filtros, favoritos e histórico
- [x] Janela de leitura integrada
- [x] Navegação por botões e setas do teclado
- [x] Zoom e redimensionamento da página
- [x] Mensagens de sucesso, erro e confirmação

</details>

<details open>
<summary><strong>7. Testes e documentação - concluída</strong></summary>

- [x] Testes de validação e cadastro
- [x] Testes de duplicidade, filtros e favoritos
- [x] Testes de progresso, histórico e persistência
- [x] Teste de leitura e ordenação CBZ
- [x] README de instalação, arquitetura e apresentação
- [x] Roteiro de demonstração acadêmica

</details>

<details>
<summary><strong>8. Próxima versão - planejada</strong></summary>

- [ ] Extração automática de capa da primeira página
- [ ] Tela de detalhes com miniatura da capa
- [ ] Visualização em página dupla
- [ ] Alternância de sentido para mangás
- [ ] Modo tela cheia
- [ ] Atalho para ir diretamente a uma página
- [ ] Notas e avaliações pessoais

</details>

<details>
<summary><strong>9. Versão avançada - futura</strong></summary>

- [ ] Persistência SQLite
- [ ] Estatísticas de leitura
- [ ] Tags personalizadas
- [ ] Importação em lote
- [ ] Metadados automáticos
- [ ] Suporte a EPUB
- [ ] Temas configuráveis

</details>

## Fluxo funcional entregue

```text
Selecionar arquivo
      ↓
Validar PDF / CBZ / CBR / CB7
      ↓
Copiar para a biblioteca
      ↓
Cadastrar metadados e persistir
      ↓
Abrir com a fábrica de leitores
      ↓
Navegar pelas páginas
      ↓
Salvar progresso e histórico
      ↓
Continuar posteriormente
```
