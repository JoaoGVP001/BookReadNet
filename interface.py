from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any

from modelos import HQ, Manga, LivroDigital, ObraDigital, StatusLeitura
from servicos import BibliotecaDigital
from validacoes import FORMATOS_ACEITOS, FORMATOS_IMAGEM


class BibliotecaApp:
    CORES = {
        "fundo": "#F1EEE6",
        "painel": "#FFFDF8",
        "escuro": "#17232D",
        "escuro_2": "#223440",
        "destaque": "#E7643B",
        "destaque_hover": "#C94C28",
        "ouro": "#D9A441",
        "texto": "#1E2A30",
        "suave": "#6B7478",
        "borda": "#D9D5CC",
    }

    def __init__(self, root: tk.Tk, biblioteca: BibliotecaDigital) -> None:
        self.root = root
        self.biblioteca = biblioteca
        self.root.title("BookReadNet | Biblioteca digital")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=self.CORES["fundo"])
        self._configurar_estilo()

        self.status_var = tk.StringVar(value="Acervo carregado.")
        self.telas: dict[str, ttk.Frame] = {}
        self.botoes_navegacao: dict[str, tk.Button] = {}
        self._construir_layout()
        self.atualizar_tudo()
        self._mostrar_tela("Acervo")

    def _configurar_estilo(self) -> None:
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=self.CORES["fundo"])
        estilo.configure("Panel.TFrame", background=self.CORES["painel"])
        estilo.configure("TLabel", background=self.CORES["fundo"], foreground=self.CORES["texto"], font=("Segoe UI", 10))
        estilo.configure("Panel.TLabel", background=self.CORES["painel"], foreground=self.CORES["texto"], font=("Segoe UI", 10))
        estilo.configure("Title.TLabel", background=self.CORES["fundo"], foreground=self.CORES["texto"], font=("Georgia", 24, "bold"))
        estilo.configure("Subtitle.TLabel", background=self.CORES["fundo"], foreground=self.CORES["suave"], font=("Segoe UI", 10))
        estilo.configure("Section.TLabel", background=self.CORES["painel"], foreground=self.CORES["texto"], font=("Georgia", 15, "bold"))
        estilo.configure("TButton", padding=(12, 8), font=("Segoe UI", 9, "bold"))
        estilo.configure("Primary.TButton", background=self.CORES["destaque"], foreground="white", borderwidth=0)
        estilo.map("Primary.TButton", background=[("active", self.CORES["destaque_hover"])])
        estilo.configure("Danger.TButton", foreground="#A53720")
        estilo.configure("Treeview", background=self.CORES["painel"], fieldbackground=self.CORES["painel"], foreground=self.CORES["texto"], rowheight=34, borderwidth=0, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", background="#E7E2D8", foreground=self.CORES["texto"], padding=8, font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview", background=[("selected", self.CORES["escuro_2"])], foreground=[("selected", "white")])
        estilo.configure("Horizontal.TProgressbar", background=self.CORES["destaque"], troughcolor="#DDD8CE")

    def _construir_layout(self) -> None:
        sidebar = tk.Frame(self.root, bg=self.CORES["escuro"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="BOOK", bg=self.CORES["escuro"], fg=self.CORES["ouro"], font=("Georgia", 13, "bold")).pack(anchor="w", padx=24, pady=(28, 0))
        tk.Label(sidebar, text="READ NET", bg=self.CORES["escuro"], fg="white", font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(0, 32))

        for nome in ("Acervo", "Continuar lendo", "Favoritos", "Histórico"):
            botao = tk.Button(
                sidebar,
                text=nome,
                command=lambda tela=nome: self._mostrar_tela(tela),
                bg=self.CORES["escuro"],
                fg="#DCE3E6",
                activebackground=self.CORES["escuro_2"],
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=24,
                pady=13,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            )
            botao.pack(fill="x")
            self.botoes_navegacao[nome] = botao

        tk.Button(
            sidebar,
            text="+  Adicionar obra",
            command=self.abrir_dialogo_cadastro,
            bg=self.CORES["destaque"],
            fg="white",
            activebackground=self.CORES["destaque_hover"],
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=11,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="bottom", fill="x", padx=20, pady=24)

        area = ttk.Frame(self.root, padding=(26, 22, 26, 10))
        area.pack(side="left", fill="both", expand=True)

        cabecalho = ttk.Frame(area)
        cabecalho.pack(fill="x", pady=(0, 18))
        ttk.Label(cabecalho, text="Sua biblioteca, no seu ritmo.", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            cabecalho,
            text="Organize e leia HQs, mangás e livros em PDF, CBZ, CBR e CB7.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        self.container = ttk.Frame(area)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._construir_tela_acervo()
        self._construir_tela_continuar()
        self._construir_tela_favoritos()
        self._construir_tela_historico()

        ttk.Label(area, textvariable=self.status_var, style="Subtitle.TLabel", anchor="w").pack(fill="x", pady=(9, 0))

    def _nova_tela(self, nome: str) -> ttk.Frame:
        frame = ttk.Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        self.telas[nome] = frame
        return frame

    def _construir_tela_acervo(self) -> None:
        tela = self._nova_tela("Acervo")
        self.busca_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value="Todos")
        self.status_filtro_var = tk.StringVar(value="Todos")

        metricas = ttk.Frame(tela)
        metricas.pack(fill="x", pady=(0, 14))
        self.total_var = tk.StringVar()
        self.lendo_var = tk.StringVar()
        self.lidos_var = tk.StringVar()
        for coluna, (rotulo, variavel) in enumerate(
            (("NO ACERVO", self.total_var), ("EM LEITURA", self.lendo_var), ("CONCLUÍDOS", self.lidos_var))
        ):
            card = tk.Frame(metricas, bg=self.CORES["painel"], highlightbackground=self.CORES["borda"], highlightthickness=1)
            card.grid(row=0, column=coluna, sticky="ew", padx=(0, 10 if coluna < 2 else 0))
            metricas.grid_columnconfigure(coluna, weight=1)
            tk.Label(card, text=rotulo, bg=self.CORES["painel"], fg=self.CORES["suave"], font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=16, pady=(12, 2))
            tk.Label(card, textvariable=variavel, bg=self.CORES["painel"], fg=self.CORES["texto"], font=("Georgia", 20, "bold")).pack(anchor="w", padx=16, pady=(0, 11))

        painel = ttk.Frame(tela, style="Panel.TFrame", padding=16)
        painel.pack(fill="both", expand=True)
        filtros = ttk.Frame(painel, style="Panel.TFrame")
        filtros.pack(fill="x", pady=(0, 12))
        ttk.Label(filtros, text="Minha biblioteca", style="Section.TLabel").pack(side="left")
        ttk.Entry(filtros, textvariable=self.busca_var, width=28).pack(side="left", padx=(24, 8))
        ttk.Combobox(filtros, textvariable=self.tipo_var, values=("Todos", "HQ", "Mangá", "Livro digital"), state="readonly", width=14).pack(side="left", padx=4)
        ttk.Combobox(
            filtros,
            textvariable=self.status_filtro_var,
            values=("Todos",) + tuple(item.value for item in StatusLeitura),
            state="readonly",
            width=14,
        ).pack(side="left", padx=4)
        ttk.Button(filtros, text="Filtrar", command=self.atualizar_acervo).pack(side="left", padx=(4, 0))

        self.arvore_acervo = self._criar_arvore(painel)
        self.arvore_acervo.bind("<Double-1>", lambda _evento: self.abrir_leitura())

        acoes = ttk.Frame(painel, style="Panel.TFrame")
        acoes.pack(fill="x", pady=(12, 0))
        ttk.Button(acoes, text="Ler / Continuar", style="Primary.TButton", command=self.abrir_leitura).pack(side="left")
        ttk.Button(acoes, text="Favoritar", command=self.alternar_favorito).pack(side="left", padx=7)
        ttk.Button(acoes, text="Editar", command=self.editar_obra).pack(side="left")
        ttk.Button(acoes, text="Excluir", style="Danger.TButton", command=self.excluir_obra).pack(side="right")

        self.busca_var.trace_add("write", lambda *_: self.atualizar_acervo())

    def _construir_tela_continuar(self) -> None:
        tela = self._nova_tela("Continuar lendo")
        painel = ttk.Frame(tela, style="Panel.TFrame", padding=18)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Continue de onde parou", style="Section.TLabel").pack(anchor="w")
        ttk.Label(painel, text="As leituras mais recentes aparecem primeiro.", style="Panel.TLabel").pack(anchor="w", pady=(4, 14))
        self.arvore_continuar = self._criar_arvore(painel)
        self.arvore_continuar.bind("<Double-1>", lambda _evento: self.abrir_leitura(self._id_selecionado(self.arvore_continuar)))
        ttk.Button(
            painel,
            text="Continuar leitura",
            style="Primary.TButton",
            command=lambda: self.abrir_leitura(self._id_selecionado(self.arvore_continuar)),
        ).pack(anchor="w", pady=(12, 0))

    def _construir_tela_favoritos(self) -> None:
        tela = self._nova_tela("Favoritos")
        painel = ttk.Frame(tela, style="Panel.TFrame", padding=18)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Obras favoritas", style="Section.TLabel").pack(anchor="w", pady=(0, 14))
        self.arvore_favoritos = self._criar_arvore(painel)
        self.arvore_favoritos.bind("<Double-1>", lambda _evento: self.abrir_leitura(self._id_selecionado(self.arvore_favoritos)))

    def _construir_tela_historico(self) -> None:
        tela = self._nova_tela("Histórico")
        painel = ttk.Frame(tela, style="Panel.TFrame", padding=18)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Histórico de leitura", style="Section.TLabel").pack(anchor="w")
        ttk.Label(painel, text="Últimas 100 páginas registradas.", style="Panel.TLabel").pack(anchor="w", pady=(4, 14))
        corpo = ttk.Frame(painel, style="Panel.TFrame")
        corpo.pack(fill="both", expand=True)
        self.lista_historico = tk.Listbox(
            corpo,
            bg=self.CORES["painel"],
            fg=self.CORES["texto"],
            selectbackground=self.CORES["escuro_2"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            activestyle="none",
        )
        self.lista_historico.pack(side="left", fill="both", expand=True)
        barra = ttk.Scrollbar(corpo, command=self.lista_historico.yview)
        barra.pack(side="right", fill="y")
        self.lista_historico.configure(yscrollcommand=barra.set)

    def _criar_arvore(self, pai: ttk.Frame) -> ttk.Treeview:
        corpo = ttk.Frame(pai, style="Panel.TFrame")
        corpo.pack(fill="both", expand=True)
        colunas = ("titulo", "autor", "tipo", "formato", "status", "progresso")
        arvore = ttk.Treeview(corpo, columns=colunas, show="headings", selectmode="browse")
        titulos = {
            "titulo": "Título",
            "autor": "Autor",
            "tipo": "Tipo",
            "formato": "Formato",
            "status": "Status",
            "progresso": "Progresso",
        }
        larguras = {"titulo": 220, "autor": 150, "tipo": 100, "formato": 70, "status": 110, "progresso": 90}
        for coluna in colunas:
            arvore.heading(coluna, text=titulos[coluna])
            arvore.column(coluna, width=larguras[coluna], minwidth=60, anchor="w", stretch=coluna in ("titulo", "autor"))
        arvore.pack(side="left", fill="both", expand=True)
        barra = ttk.Scrollbar(corpo, command=arvore.yview)
        barra.pack(side="right", fill="y")
        arvore.configure(yscrollcommand=barra.set)
        return arvore

    def _mostrar_tela(self, nome: str) -> None:
        nome_real = "Favoritos" if nome == "Favoritos" else nome
        self.telas[nome_real].tkraise()
        for titulo, botao in self.botoes_navegacao.items():
            botao.configure(bg=self.CORES["escuro_2"] if titulo == nome else self.CORES["escuro"])
        self.atualizar_tudo()

    def atualizar_tudo(self) -> None:
        self.atualizar_acervo()
        self._preencher_arvore(self.arvore_continuar, self.biblioteca.continuar_lendo())
        self._preencher_arvore(self.arvore_favoritos, self.biblioteca.filtrar(somente_favoritos=True))
        self.lista_historico.delete(0, tk.END)
        for linha in self.biblioteca.listar_historico():
            self.lista_historico.insert(tk.END, linha)
        obras = self.biblioteca.obras
        self.total_var.set(str(len(obras)))
        self.lendo_var.set(str(sum(obra.status_leitura == StatusLeitura.EM_LEITURA for obra in obras)))
        self.lidos_var.set(str(sum(obra.status_leitura == StatusLeitura.LIDO for obra in obras)))

    def atualizar_acervo(self) -> None:
        obras = self.biblioteca.filtrar(
            termo=self.busca_var.get(),
            tipo=self.tipo_var.get(),
            status=self.status_filtro_var.get(),
        )
        self._preencher_arvore(self.arvore_acervo, obras)

    def _preencher_arvore(self, arvore: ttk.Treeview, obras: list[ObraDigital]) -> None:
        arvore.delete(*arvore.get_children())
        for obra in obras:
            progresso = self.biblioteca.obter_progresso(obra.id_obra)
            marcador = "★ " if obra.favorito else ""
            texto_progresso = f"{progresso.porcentagem:.1f}%" if progresso.total_paginas else "0%"
            arvore.insert(
                "",
                tk.END,
                iid=obra.id_obra,
                values=(
                    marcador + obra.titulo,
                    obra.autor,
                    obra.obter_tipo(),
                    obra.formato,
                    obra.status_leitura.value,
                    texto_progresso,
                ),
            )

    @staticmethod
    def _id_selecionado(arvore: ttk.Treeview) -> str | None:
        selecao = arvore.selection()
        return selecao[0] if selecao else None

    def _obra_selecionada(self) -> ObraDigital | None:
        id_obra = self._id_selecionado(self.arvore_acervo)
        if not id_obra:
            messagebox.showwarning("Seleção necessária", "Selecione uma obra no acervo.")
            return None
        return self.biblioteca.buscar_por_id(id_obra)

    def abrir_dialogo_cadastro(self) -> None:
        self._dialogo_obra()

    def editar_obra(self) -> None:
        obra = self._obra_selecionada()
        if obra:
            self._dialogo_obra(obra)

    def _dialogo_obra(self, obra: ObraDigital | None = None) -> None:
        janela = tk.Toplevel(self.root)
        janela.title("Editar obra" if obra else "Adicionar obra")
        janela.geometry("650x620")
        janela.resizable(False, False)
        janela.configure(bg=self.CORES["fundo"])
        janela.transient(self.root)
        janela.grab_set()

        painel = ttk.Frame(janela, style="Panel.TFrame", padding=22)
        painel.pack(fill="both", expand=True, padx=18, pady=18)
        ttk.Label(painel, text="Editar metadados" if obra else "Nova obra digital", style="Section.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        vars_form = {
            "titulo": tk.StringVar(value=obra.titulo if obra else ""),
            "autor": tk.StringVar(value=obra.autor if obra else ""),
            "tipo": tk.StringVar(value=obra.obter_tipo() if obra else "Mangá"),
            "categoria": tk.StringVar(value=obra.categoria if obra else ""),
            "serie": tk.StringVar(value=obra.serie if obra else ""),
            "editora": tk.StringVar(value=obra.editora if obra else ""),
            "idioma": tk.StringVar(value=obra.idioma if obra else "Português"),
            "detalhe": tk.StringVar(value=self._detalhe_obra(obra) if obra else ""),
            "arquivo": tk.StringVar(value=obra.caminho_arquivo if obra else ""),
            "capa": tk.StringVar(value=obra.caminho_capa if obra else ""),
        }
        detalhe_label = tk.StringVar()

        campos = (
            ("Título *", "titulo"),
            ("Autor", "autor"),
            ("Tipo", "tipo"),
            ("Categoria", "categoria"),
            ("Série", "serie"),
            ("Editora", "editora"),
            ("Idioma", "idioma"),
        )
        for linha, (rotulo, chave) in enumerate(campos, start=1):
            ttk.Label(painel, text=rotulo, style="Panel.TLabel").grid(row=linha, column=0, sticky="w", pady=6, padx=(0, 12))
            if chave == "tipo":
                widget = ttk.Combobox(painel, textvariable=vars_form[chave], values=tuple(self.biblioteca.TIPOS_OBRA), state="disabled" if obra else "readonly", width=39)
            else:
                widget = ttk.Entry(painel, textvariable=vars_form[chave], width=42)
            widget.grid(row=linha, column=1, columnspan=2, sticky="ew", pady=6)

        ttk.Label(painel, textvariable=detalhe_label, style="Panel.TLabel").grid(row=8, column=0, sticky="w", pady=6, padx=(0, 12))
        ttk.Entry(painel, textvariable=vars_form["detalhe"], width=42).grid(row=8, column=1, columnspan=2, sticky="ew", pady=6)

        ttk.Label(painel, text="Arquivo *", style="Panel.TLabel").grid(row=9, column=0, sticky="w", pady=6, padx=(0, 12))
        ttk.Entry(painel, textvariable=vars_form["arquivo"], state="readonly", width=34).grid(row=9, column=1, sticky="ew", pady=6)
        ttk.Button(painel, text="Selecionar", state="disabled" if obra else "normal", command=lambda: self._selecionar_arquivo(vars_form)).grid(row=9, column=2, padx=(8, 0))

        ttk.Label(painel, text="Capa", style="Panel.TLabel").grid(row=10, column=0, sticky="w", pady=6, padx=(0, 12))
        ttk.Entry(painel, textvariable=vars_form["capa"], state="readonly", width=34).grid(row=10, column=1, sticky="ew", pady=6)
        ttk.Button(painel, text="Selecionar", state="disabled" if obra else "normal", command=lambda: self._selecionar_capa(vars_form)).grid(row=10, column=2, padx=(8, 0))

        def atualizar_detalhe(*_args: Any) -> None:
            detalhe_label.set({"HQ": "Nº da edição", "Mangá": "Volume", "Livro digital": "Edição"}.get(vars_form["tipo"].get(), "Detalhe"))

        vars_form["tipo"].trace_add("write", atualizar_detalhe)
        atualizar_detalhe()

        def salvar() -> None:
            try:
                especifico = self._dados_especificos(vars_form["tipo"].get(), vars_form["detalhe"].get())
                if obra:
                    self.biblioteca.editar_obra(
                        obra.id_obra,
                        titulo=vars_form["titulo"].get(),
                        autor=vars_form["autor"].get(),
                        categoria=vars_form["categoria"].get(),
                        serie=vars_form["serie"].get(),
                        editora=vars_form["editora"].get(),
                        idioma=vars_form["idioma"].get(),
                        **especifico,
                    )
                    mensagem = "Obra atualizada com sucesso."
                else:
                    self.biblioteca.cadastrar_obra(
                        tipo=vars_form["tipo"].get(),
                        titulo=vars_form["titulo"].get(),
                        autor=vars_form["autor"].get(),
                        categoria=vars_form["categoria"].get(),
                        serie=vars_form["serie"].get(),
                        editora=vars_form["editora"].get(),
                        idioma=vars_form["idioma"].get(),
                        caminho_arquivo=vars_form["arquivo"].get(),
                        caminho_capa=vars_form["capa"].get(),
                        **especifico,
                    )
                    mensagem = "Obra importada para o acervo."
                self.status_var.set(mensagem)
                self.atualizar_tudo()
                janela.destroy()
                messagebox.showinfo("BookReadNet", mensagem)
            except (OSError, RuntimeError, ValueError) as erro:
                messagebox.showerror("Não foi possível salvar", str(erro), parent=janela)

        painel.grid_columnconfigure(1, weight=1)
        botoes = ttk.Frame(painel, style="Panel.TFrame")
        botoes.grid(row=11, column=0, columnspan=3, sticky="e", pady=(20, 0))
        ttk.Button(botoes, text="Cancelar", command=janela.destroy).pack(side="left", padx=(0, 8))
        ttk.Button(botoes, text="Salvar obra", style="Primary.TButton", command=salvar).pack(side="left")

    def _selecionar_arquivo(self, vars_form: dict[str, tk.StringVar]) -> None:
        tipos = [("Quadrinhos e documentos", " ".join(f"*{item}" for item in FORMATOS_ACEITOS)), ("Todos", "*.*")]
        caminho = filedialog.askopenfilename(title="Selecionar obra", filetypes=tipos, parent=self.root)
        if caminho:
            vars_form["arquivo"].set(caminho)
            if not vars_form["titulo"].get().strip():
                vars_form["titulo"].set(Path(caminho).stem.replace("_", " "))

    def _selecionar_capa(self, vars_form: dict[str, tk.StringVar]) -> None:
        caminho = filedialog.askopenfilename(
            title="Selecionar capa",
            filetypes=[("Imagens", " ".join(f"*{item}" for item in FORMATOS_IMAGEM)), ("Todos", "*.*")],
            parent=self.root,
        )
        if caminho:
            vars_form["capa"].set(caminho)

    @staticmethod
    def _dados_especificos(tipo: str, detalhe: str) -> dict[str, str]:
        return {
            "HQ": {"numero_edicao": detalhe},
            "Mangá": {"volume": detalhe},
            "Livro digital": {"edicao": detalhe},
        }.get(tipo, {})

    @staticmethod
    def _detalhe_obra(obra: ObraDigital | None) -> str:
        if isinstance(obra, HQ):
            return obra.numero_edicao
        if isinstance(obra, Manga):
            return obra.volume
        if isinstance(obra, LivroDigital):
            return obra.edicao
        return ""

    def alternar_favorito(self) -> None:
        obra = self._obra_selecionada()
        if not obra:
            return
        favorito = self.biblioteca.alternar_favorito(obra.id_obra)
        self.status_var.set("Adicionado aos favoritos." if favorito else "Removido dos favoritos.")
        self.atualizar_tudo()

    def excluir_obra(self) -> None:
        obra = self._obra_selecionada()
        if not obra:
            return
        if not messagebox.askyesno("Excluir obra", f"Remover '{obra.titulo}' do acervo?"):
            return
        excluir_arquivo = messagebox.askyesno(
            "Arquivo físico",
            "Deseja também excluir a cópia do arquivo armazenada pelo BookReadNet?",
        )
        try:
            self.biblioteca.excluir_obra(obra.id_obra, excluir_arquivo)
            self.status_var.set("Obra excluída do acervo.")
            self.atualizar_tudo()
        except (OSError, ValueError) as erro:
            messagebox.showerror("Falha ao excluir", str(erro))

    def abrir_leitura(self, id_obra: str | None = None) -> None:
        if not id_obra:
            id_obra = self._id_selecionado(self.arvore_acervo)
        if not id_obra:
            messagebox.showwarning("Seleção necessária", "Selecione uma obra para ler.")
            return
        try:
            obra = self.biblioteca.buscar_por_id(id_obra)
            leitor = self.biblioteca.criar_leitor(id_obra)
            JanelaLeitura(self.root, self.biblioteca, obra, leitor, self.atualizar_tudo)
            self.status_var.set(f"Leitura aberta: {obra.titulo}")
        except (OSError, RuntimeError, ValueError) as erro:
            messagebox.showerror("Não foi possível abrir a obra", str(erro))


class JanelaLeitura:
    def __init__(
        self,
        root: tk.Tk,
        biblioteca: BibliotecaDigital,
        obra: ObraDigital,
        leitor: Any,
        ao_fechar: Any,
    ) -> None:
        self.biblioteca = biblioteca
        self.obra = obra
        self.leitor = leitor
        self.ao_fechar = ao_fechar
        self.zoom = 1.0
        self.imagem_original: Any = None
        self.foto: Any = None
        self._redimensionamento_id: str | None = None

        progresso = biblioteca.obter_progresso(obra.id_obra)
        self.pagina = min(max(progresso.pagina_atual - 1, 0), leitor.total_paginas - 1)

        self.janela = tk.Toplevel(root)
        self.janela.title(f"Lendo | {obra.titulo}")
        self.janela.geometry("1120x780")
        self.janela.minsize(760, 560)
        self.janela.configure(bg="#10171C")
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)

        barra = tk.Frame(self.janela, bg="#17232D", height=62)
        barra.pack(fill="x")
        tk.Label(barra, text=obra.titulo, bg="#17232D", fg="white", font=("Georgia", 14, "bold")).pack(side="left", padx=18)
        tk.Button(barra, text="← Anterior", command=self.anterior, **self._estilo_botao()).pack(side="left", padx=(18, 5), pady=12)
        tk.Button(barra, text="Próxima →", command=self.proxima, **self._estilo_botao()).pack(side="left", padx=5, pady=12)

        self.pagina_var = tk.StringVar()
        tk.Label(barra, textvariable=self.pagina_var, bg="#17232D", fg="#D9A441", font=("Segoe UI", 10, "bold")).pack(side="left", padx=16)
        tk.Button(barra, text="−", command=self.reduzir_zoom, **self._estilo_botao()).pack(side="right", padx=(4, 18), pady=12)
        tk.Button(barra, text="+", command=self.aumentar_zoom, **self._estilo_botao()).pack(side="right", padx=4, pady=12)
        self.zoom_var = tk.StringVar(value="100%")
        tk.Label(barra, textvariable=self.zoom_var, bg="#17232D", fg="#DCE3E6", font=("Segoe UI", 9)).pack(side="right", padx=8)

        corpo = tk.Frame(self.janela, bg="#10171C")
        corpo.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(corpo, bg="#10171C", highlightthickness=0)
        barra_y = ttk.Scrollbar(corpo, orient="vertical", command=self.canvas.yview)
        barra_x = ttk.Scrollbar(corpo, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        barra_y.pack(side="right", fill="y")
        barra_x.pack(side="bottom", fill="x")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self._agendar_redimensionamento)
        self.janela.bind("<Left>", lambda _evento: self.anterior())
        self.janela.bind("<Right>", lambda _evento: self.proxima())
        self.janela.bind("<Escape>", lambda _evento: self.fechar())
        self._carregar_pagina()

    @staticmethod
    def _estilo_botao() -> dict[str, Any]:
        return {
            "bg": "#223440",
            "fg": "white",
            "activebackground": "#E7643B",
            "activeforeground": "white",
            "relief": "flat",
            "padx": 11,
            "pady": 7,
            "font": ("Segoe UI", 9, "bold"),
            "cursor": "hand2",
        }

    def _carregar_pagina(self) -> None:
        try:
            self.imagem_original = self.leitor.obter_pagina(self.pagina)
            self._renderizar()
            pagina_humana = self.pagina + 1
            self.pagina_var.set(f"Página {pagina_humana} de {self.leitor.total_paginas}")
            self.biblioteca.salvar_progresso(self.obra.id_obra, pagina_humana, self.leitor.total_paginas)
        except (OSError, RuntimeError, ValueError) as erro:
            messagebox.showerror("Erro de leitura", str(erro), parent=self.janela)

    def _renderizar(self) -> None:
        if self.imagem_original is None:
            return
        from PIL import Image, ImageTk

        largura_area = max(self.canvas.winfo_width() - 40, 300)
        altura_area = max(self.canvas.winfo_height() - 40, 300)
        escala_base = min(largura_area / self.imagem_original.width, altura_area / self.imagem_original.height)
        escala = max(0.1, escala_base * self.zoom)
        tamanho = (
            max(1, int(self.imagem_original.width * escala)),
            max(1, int(self.imagem_original.height * escala)),
        )
        imagem = self.imagem_original.resize(tamanho, Image.Resampling.LANCZOS)
        self.foto = ImageTk.PhotoImage(imagem)
        self.canvas.delete("pagina")
        x = max(largura_area // 2 + 20, tamanho[0] // 2 + 20)
        y = max(altura_area // 2 + 20, tamanho[1] // 2 + 20)
        self.canvas.create_image(x, y, image=self.foto, anchor="center", tags="pagina")
        self.canvas.configure(scrollregion=(0, 0, max(largura_area + 40, tamanho[0] + 40), max(altura_area + 40, tamanho[1] + 40)))
        self.zoom_var.set(f"{int(self.zoom * 100)}%")

    def _agendar_redimensionamento(self, _evento: tk.Event[Any]) -> None:
        if self._redimensionamento_id:
            self.janela.after_cancel(self._redimensionamento_id)
        self._redimensionamento_id = self.janela.after(150, self._renderizar)

    def anterior(self) -> None:
        if self.pagina > 0:
            self.pagina -= 1
            self._carregar_pagina()

    def proxima(self) -> None:
        if self.pagina < self.leitor.total_paginas - 1:
            self.pagina += 1
            self._carregar_pagina()

    def aumentar_zoom(self) -> None:
        self.zoom = min(3.0, self.zoom + 0.2)
        self._renderizar()

    def reduzir_zoom(self) -> None:
        self.zoom = max(0.4, self.zoom - 0.2)
        self._renderizar()

    def fechar(self) -> None:
        try:
            self.leitor.fechar()
        finally:
            self.ao_fechar()
            self.janela.destroy()
