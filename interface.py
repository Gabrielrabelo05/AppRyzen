# """
# interface.py — Componentes visuais da UI (CustomTkinter).
# """

# import customtkinter as ctk
# from tkinter import filedialog, messagebox
# import threading
# import os

# from exec import carregar_planilha, analisar, gerar_relatorio


# # ──────────────────────────────────────────────
# # Configuração global de aparência
# # ──────────────────────────────────────────────
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")

# AZUL_ACENTO  = "#3B82F6"
# VERDE_OK     = "#22C55E"
# AMARELO_WARN = "#F59E0B"
# CINZA_BG     = "#1E1E2E"
# CINZA_CARD   = "#2A2A3E"
# CINZA_BORDA  = "#3A3A55"
# BRANCO       = "#E2E8F0"
# FONTE_MONO   = ("Consolas", 12)
# FONTE_TITULO = ("Segoe UI", 22, "bold")
# FONTE_NORMAL = ("Segoe UI", 13)
# FONTE_SMALL  = ("Segoe UI", 11)


# # ──────────────────────────────────────────────
# # Widget de tabela simples (grade ScrollFrame)
# # ──────────────────────────────────────────────

# class TabelaResumo(ctk.CTkScrollableFrame):
#     """Grade de linhas e colunas para exibir o resumo dos dados."""

#     def __init__(self, master, cabecalho: list[str], linhas: list[list], **kw):
#         super().__init__(master, **kw)
#         self._construir(cabecalho, linhas)

#     def _construir(self, cabecalho, linhas):
#         cores_alt = [CINZA_CARD, "#252538"]

#         # Cabeçalho
#         for col, texto in enumerate(cabecalho):
#             ctk.CTkLabel(
#                 self, text=texto, font=("Segoe UI", 12, "bold"),
#                 text_color=AZUL_ACENTO, anchor="w",
#                 fg_color=CINZA_BG, corner_radius=0,
#             ).grid(row=0, column=col, sticky="ew", padx=(0, 2), pady=(0, 2))
#             self.columnconfigure(col, weight=1)

#         # Linhas de dados
#         for r_idx, linha in enumerate(linhas, start=1):
#             bg = cores_alt[r_idx % 2]
#             for c_idx, celula in enumerate(linha):
#                 ctk.CTkLabel(
#                     self, text=str(celula), font=FONTE_SMALL,
#                     text_color=BRANCO, anchor="w",
#                     fg_color=bg, corner_radius=0,
#                 ).grid(row=r_idx, column=c_idx, sticky="ew", padx=(0, 2), pady=1)


# # ──────────────────────────────────────────────
# # Janela principal
# # ──────────────────────────────────────────────

# class AppRyzen(ctk.CTk):

#     def __init__(self):
#         super().__init__()
#         self.title("Ryzen Analyzer — Análise de Dados de Pesquisa")
#         self.geometry("1100x750")
#         self.minsize(900, 600)
#         self.configure(fg_color=CINZA_BG)

#         self._df         = None
#         self._resultados = None
#         self._caminho    = None

#         self._construir_layout()

#     # ── Layout principal ──────────────────────

#     def _construir_layout(self):
#         # Barra lateral esquerda
#         self._sidebar = ctk.CTkFrame(self, width=240, fg_color=CINZA_CARD,
#                                      corner_radius=0)
#         self._sidebar.pack(side="left", fill="y")
#         self._sidebar.pack_propagate(False)

#         # Área de conteúdo
#         self._content = ctk.CTkFrame(self, fg_color=CINZA_BG, corner_radius=0)
#         self._content.pack(side="right", fill="both", expand=True)

#         self._montar_sidebar()
#         self._montar_tela_inicial()

#     def _montar_sidebar(self):
#         sb = self._sidebar

#         # Logo / título
#         ctk.CTkLabel(sb, text="⚡ RYZEN", font=("Segoe UI", 20, "bold"),
#                      text_color=AZUL_ACENTO).pack(pady=(28, 2))
#         ctk.CTkLabel(sb, text="Analyzer", font=("Segoe UI", 13),
#                      text_color=BRANCO).pack()

#         ctk.CTkLabel(sb, text="─" * 28, text_color=CINZA_BORDA,
#                      font=("Segoe UI", 10)).pack(pady=12)

#         # Botão selecionar planilha
#         self._btn_selecionar = ctk.CTkButton(
#             sb, text="📂  Selecionar Planilha",
#             font=FONTE_NORMAL, height=44,
#             fg_color=AZUL_ACENTO, hover_color="#2563EB",
#             corner_radius=10,
#             command=self._selecionar_arquivo,
#         )
#         self._btn_selecionar.pack(padx=16, pady=6, fill="x")

#         # Botão analisar
#         self._btn_analisar = ctk.CTkButton(
#             sb, text="🔍  Analisar Dados",
#             font=FONTE_NORMAL, height=44,
#             fg_color="#7C3AED", hover_color="#6D28D9",
#             corner_radius=10, state="disabled",
#             command=self._iniciar_analise,
#         )
#         self._btn_analisar.pack(padx=16, pady=6, fill="x")

#         ctk.CTkLabel(sb, text="─" * 28, text_color=CINZA_BORDA,
#                      font=("Segoe UI", 10)).pack(pady=12)

#         # Botão baixar relatório
#         self._btn_relatorio = ctk.CTkButton(
#             sb, text="⬇  Baixar Relatório .txt",
#             font=FONTE_NORMAL, height=44,
#             fg_color="#059669", hover_color="#047857",
#             corner_radius=10, state="disabled",
#             command=self._baixar_relatorio,
#         )
#         self._btn_relatorio.pack(padx=16, pady=6, fill="x")

#         # Espaçador + info arquivo
#         ctk.CTkLabel(sb, text="─" * 28, text_color=CINZA_BORDA,
#                      font=("Segoe UI", 10)).pack(pady=12)
#         self._lbl_arquivo = ctk.CTkLabel(
#             sb, text="Nenhum arquivo\nselecionado.",
#             font=FONTE_SMALL, text_color="#94A3B8",
#             wraplength=200, justify="center",
#         )
#         self._lbl_arquivo.pack(padx=10)

#     def _montar_tela_inicial(self):
#         for w in self._content.winfo_children():
#             w.destroy()

#         frame = ctk.CTkFrame(self._content, fg_color="transparent")
#         frame.place(relx=0.5, rely=0.45, anchor="center")

#         ctk.CTkLabel(frame, text="📊", font=("Segoe UI", 64)).pack()
#         ctk.CTkLabel(frame, text="Ryzen Field Research Analyzer",
#                      font=FONTE_TITULO, text_color=BRANCO).pack(pady=(8, 4))
#         ctk.CTkLabel(
#             frame,
#             text="Selecione uma planilha Excel (.xlsx) para iniciar a análise.",
#             font=FONTE_NORMAL, text_color="#94A3B8",
#         ).pack()

#     # ── Ações ─────────────────────────────────

#     def _selecionar_arquivo(self):
#         caminho = filedialog.askopenfilename(
#             title="Selecione a planilha",
#             filetypes=[("Excel", "*.xlsx *.xls"), ("Todos", "*.*")],
#         )
#         if not caminho:
#             return

#         self._caminho = caminho
#         nome = os.path.basename(caminho)
#         self._lbl_arquivo.configure(text=f"📄 {nome}")
#         self._btn_analisar.configure(state="normal")
#         self._btn_relatorio.configure(state="disabled")
#         self._df = None
#         self._resultados = None
#         self._montar_tela_inicial()

#     def _iniciar_analise(self):
#         self._btn_analisar.configure(state="disabled", text="Processando...")
#         self._btn_selecionar.configure(state="disabled")
#         self._montar_tela_log()
#         threading.Thread(target=self._executar_analise, daemon=True).start()

#     def _executar_analise(self):
#         try:
#             df, log_carga = carregar_planilha(self._caminho)
#             for msg in log_carga:
#                 self._append_log(msg)

#             res, log_anal = analisar(df)
#             for msg in log_anal:
#                 self._append_log(msg)

#             self._df         = df
#             self._resultados = res
#             self.after(300, self._mostrar_resultados)

#         except Exception as e:
#             self.after(0, lambda: messagebox.showerror("Erro", str(e)))
#             self.after(0, self._resetar_botoes)

#     def _resetar_botoes(self):
#         self._btn_analisar.configure(state="normal", text="🔍  Analisar Dados")
#         self._btn_selecionar.configure(state="normal")

#     # ── Tela de log ───────────────────────────

#     def _montar_tela_log(self):
#         for w in self._content.winfo_children():
#             w.destroy()

#         ctk.CTkLabel(self._content, text="Processando...",
#                      font=FONTE_TITULO, text_color=BRANCO).pack(pady=(24, 8))

#         self._log_box = ctk.CTkTextbox(
#             self._content, font=FONTE_MONO,
#             fg_color=CINZA_CARD, text_color=VERDE_OK,
#             border_color=CINZA_BORDA, border_width=1,
#             corner_radius=10, wrap="word",
#         )
#         self._log_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
#         self._log_box.configure(state="disabled")

#     def _append_log(self, msg: str):
#         def _do():
#             self._log_box.configure(state="normal")
#             self._log_box.insert("end", msg + "\n")
#             self._log_box.see("end")
#             self._log_box.configure(state="disabled")
#         self.after(0, _do)

#     # ── Tela de resultados ────────────────────

#     def _mostrar_resultados(self):
#         for w in self._content.winfo_children():
#             w.destroy()

#         r = self._resultados

#         # Cabeçalho
#         header = ctk.CTkFrame(self._content, fg_color="transparent")
#         header.pack(fill="x", padx=20, pady=(20, 8))
#         ctk.CTkLabel(header, text="Resultados da Análise",
#                      font=FONTE_TITULO, text_color=BRANCO).pack(side="left")

#         # ── Linha 1 de cards: métricas rápidas ──
#         cards = ctk.CTkFrame(self._content, fg_color="transparent")
#         cards.pack(fill="x", padx=20, pady=4)

#         metricas = [
#             ("📋 Respostas",          str(r["total_respostas"])),
#             ("📈 Preparo médio",      f"{r['preparo_media']} / 5"),
#             ("💻 Usaria plataforma",  f"{r['plataforma_pct_sim']}%"),
#             ("💼 Já estagia",         f"{r['estagio_pct_sim']}%"),
#         ]
#         for icone_label, valor in metricas:
#             self._card(cards, icone_label, valor).pack(
#                 side="left", expand=True, fill="both", padx=4, pady=4)

#         # ── Linha 2 de cards: Faixa de preço + Atributo mais valorizado ──
#         cards2 = ctk.CTkFrame(self._content, fg_color="transparent")
#         cards2.pack(fill="x", padx=20, pady=(0, 4))

#         faixa     = r.get("faixa_preco_adequada", "—")
#         faixa_pct = r.get("faixa_preco_pct", 0)
#         self._card(
#             cards2,
#             "💰 Faixa de preço mais adequada",
#             f"{faixa}  ({faixa_pct}%)"
#         ).pack(side="left", expand=True, fill="both", padx=4, pady=4)

#         atrib     = r.get("atributo_top1", "—")
#         atrib_pct = r.get("atributo_top1_pct", 0)
#         # trunca texto longo para não estourar o card
#         atrib_display = (atrib[:38] + "…") if len(atrib) > 40 else atrib
#         self._card(
#             cards2,
#             "⭐ Atributo mais valorizado",
#             f"{atrib_display}  ({atrib_pct}%)"
#         ).pack(side="left", expand=True, fill="both", padx=4, pady=4)

#         # ── Abas (notebook) ──
#         tabview = ctk.CTkTabview(
#             self._content,
#             fg_color=CINZA_CARD,
#             segmented_button_fg_color=CINZA_BG,
#             segmented_button_selected_color=AZUL_ACENTO,
#             segmented_button_unselected_color=CINZA_CARD,
#             segmented_button_selected_hover_color="#2563EB",
#             corner_radius=10,
#         )
#         tabview.pack(fill="both", expand=True, padx=20, pady=(4, 16))

#         abas = [
#             ("Resumo Geral",      self._aba_resumo),
#             ("Cursos & Períodos", self._aba_cursos),
#             ("Medos",             self._aba_medos),
#             ("Plataforma",        self._aba_plataforma),
#             ("Preparo Técnico",   self._aba_preparo),
#         ]
#         for nome, construtor in abas:
#             tabview.add(nome)
#             construtor(tabview.tab(nome), r)

#         # Habilitar download
#         self._btn_analisar.configure(state="normal", text="🔍  Analisar Dados")
#         self._btn_selecionar.configure(state="normal")
#         self._btn_relatorio.configure(state="normal")

#     # ── Utilitário card ───────────────────────

#     def _card(self, master, titulo, valor):
#         f = ctk.CTkFrame(master, fg_color=CINZA_CARD, corner_radius=12,
#                          border_color=CINZA_BORDA, border_width=1)
#         ctk.CTkLabel(f, text=titulo, font=FONTE_SMALL,
#                      text_color="#94A3B8").pack(padx=16, pady=(12, 0))
#         ctk.CTkLabel(f, text=valor, font=("Segoe UI", 20, "bold"),
#                      text_color=AZUL_ACENTO, wraplength=300).pack(padx=16, pady=(0, 12))
#         return f

#     # ── Conteúdo das abas ─────────────────────

#     def _aba_resumo(self, parent, r):
#         cab = ["Indicador", "Valor"]
#         linhas = [
#             ["Total de respostas",             r["total_respostas"]],
#             ["Período de coleta",              r["periodo_coleta"]],
#             ["Preparo técnico médio",          f"{r['preparo_media']} / 5"],
#             ["Preparo técnico mediana",        f"{r['preparo_mediana']} / 5"],
#             ["Desvio padrão (preparo)",        r["preparo_desvio"]],
#             ["Estudantes c/ estágio/emprego",  f"{r['estagio_pct_sim']}%"],
#             ["Usariam a plataforma",           f"{r['plataforma_pct_sim']}%"],
#             ["Faixa de preço mais adequada",   f"{r.get('faixa_preco_adequada','—')} ({r.get('faixa_preco_pct',0)}%)"],
#             ["Atributo mais valorizado",       f"{r.get('atributo_top1','—')} ({r.get('atributo_top1_pct',0)}%)"],
#         ]
#         TabelaResumo(parent, cab, linhas, fg_color=CINZA_CARD,
#                      corner_radius=8).pack(fill="both", expand=True, padx=8, pady=8)

#     def _aba_cursos(self, parent, r):
#         total = r["total_respostas"]
#         cab = ["Curso", "Respostas", "% do total"]
#         linhas_c = [
#             [k, v, f"{round(v/total*100,1)}%"]
#             for k, v in sorted(r["cursos"].items(), key=lambda x: -x[1])
#         ]
#         cab_p = ["Período", "Respostas", "% do total"]
#         linhas_p = [
#             [k, v, f"{round(v/total*100,1)}%"]
#             for k, v in sorted(r["periodos"].items(), key=lambda x: -x[1])
#         ]
#         ctk.CTkLabel(parent, text="Cursos", font=("Segoe UI", 13, "bold"),
#                      text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(8, 2))
#         TabelaResumo(parent, cab, linhas_c, fg_color=CINZA_CARD,
#                      corner_radius=8, height=160).pack(fill="x", padx=8)
#         ctk.CTkLabel(parent, text="Períodos", font=("Segoe UI", 13, "bold"),
#                      text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(12, 2))
#         TabelaResumo(parent, cab_p, linhas_p, fg_color=CINZA_CARD,
#                      corner_radius=8, height=180).pack(fill="both", expand=True, padx=8, pady=(0, 8))

#     def _aba_medos(self, parent, r):
#         total_mencoes = sum(r["medos"].values())
#         cab = ["Medo", "Menções", "% das menções"]
#         linhas = [
#             [k, v, f"{round(v/total_mencoes*100,1)}%"]
#             for k, v in r["medos"].items()
#         ]
#         TabelaResumo(parent, cab, linhas, fg_color=CINZA_CARD,
#                      corner_radius=8).pack(fill="both", expand=True, padx=8, pady=8)

#     def _aba_plataforma(self, parent, r):
#         total = r["total_respostas"]

#         cab1 = ["Usaria a plataforma?", "Respostas", "%"]
#         lin1 = [
#             [k, v, f"{round(v/total*100,1)}%"]
#             for k, v in r["usaria_plataforma"].items()
#         ]

#         cab2 = ["Investimento mensal", "Respostas", "%"]
#         lin2 = [
#             [k, v, f"{round(v/total*100,1)}%"]
#             for k, v in sorted(r["investimento"].items(), key=lambda x: -x[1])
#         ]

#         cab3 = ["Funcionalidade valiosa", "Respostas", "%"]
#         lin3 = [
#             [k, v, f"{round(v/total*100,1)}%"]
#             for k, v in sorted(r["atributos_valorizados"].items(), key=lambda x: -x[1])
#         ]

#         ctk.CTkLabel(parent, text="Uso da plataforma", font=("Segoe UI", 13, "bold"),
#                      text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(8, 2))
#         TabelaResumo(parent, cab1, lin1, fg_color=CINZA_CARD,
#                      corner_radius=8, height=110).pack(fill="x", padx=8)

#         ctk.CTkLabel(parent, text="Disposição de investimento", font=("Segoe UI", 13, "bold"),
#                      text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(10, 2))
#         TabelaResumo(parent, cab2, lin2, fg_color=CINZA_CARD,
#                      corner_radius=8, height=130).pack(fill="x", padx=8)

#         ctk.CTkLabel(parent, text="Funcionalidades mais valorizadas", font=("Segoe UI", 13, "bold"),
#                      text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(10, 2))
#         TabelaResumo(parent, cab3, lin3, fg_color=CINZA_CARD,
#                      corner_radius=8).pack(fill="both", expand=True, padx=8, pady=(0, 8))

#     def _aba_preparo(self, parent, r):
#         total = r["total_respostas"]
#         cab = ["Nota (1–5)", "Qtd. respostas", "% do total", "Barra visual"]
#         max_v = max(r["preparo_dist"].values(), default=1)
#         linhas = []
#         for nota in sorted(r["preparo_dist"]):
#             v = r["preparo_dist"][nota]
#             barra = "█" * int(v * 20 / max_v)
#             linhas.append([
#                 f"  {int(nota)}  ",
#                 v,
#                 f"{round(v/total*100,1)}%",
#                 barra,
#             ])
#         TabelaResumo(parent, cab, linhas, fg_color=CINZA_CARD,
#                      corner_radius=8, height=220).pack(fill="x", padx=8, pady=8)

#         info = ctk.CTkFrame(parent, fg_color=CINZA_CARD, corner_radius=10)
#         info.pack(fill="x", padx=8, pady=4)
#         stats = [
#             ("Média",         r["preparo_media"]),
#             ("Mediana",       r["preparo_mediana"]),
#             ("Desvio padrão", r["preparo_desvio"]),
#         ]
#         for lbl, val in stats:
#             row = ctk.CTkFrame(info, fg_color="transparent")
#             row.pack(fill="x", padx=16, pady=4)
#             ctk.CTkLabel(row, text=lbl, font=FONTE_SMALL,
#                          text_color="#94A3B8").pack(side="left")
#             ctk.CTkLabel(row, text=str(val), font=("Segoe UI", 13, "bold"),
#                          text_color=VERDE_OK).pack(side="right")

#     # ── Download .txt ─────────────────────────

#     def _baixar_relatorio(self):
#         if not self._resultados:
#             messagebox.showwarning("Aviso", "Nenhuma análise disponível.")
#             return

#         dest = filedialog.asksaveasfilename(
#             title="Salvar relatório",
#             defaultextension=".txt",
#             filetypes=[("Texto", "*.txt")],
#             initialfile="relatorio_ryzen.txt",
#         )
#         if not dest:
#             return

#         try:
#             gerar_relatorio(self._df, self._resultados, dest)
#             messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{dest}")
#         except Exception as e:
#             messagebox.showerror("Erro ao salvar", str(e))




















"""
interface.py — Componentes visuais da UI (CustomTkinter). Tema: Branco + Azul Marinho.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

from exec import carregar_planilha, analisar, gerar_relatorio


# ──────────────────────────────────────────────
# Configuração global de aparência
# ──────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Paleta de cores ──
AZUL_MARINHO  = "#1E3A5F"   # sidebar
AZUL_ACENTO   = "#2563EB"   # botões, destaques
AZUL_HOVER    = "#1D4ED8"   # hover botões
AZUL_CLARO    = "#DBEAFE"   # fundo cabeçalho tabela
AZUL_TEXTO    = "#1E40AF"   # texto de destaque nos cards
CINZA_BG      = "#F0F4F8"   # fundo principal
BRANCO        = "#FFFFFF"   # cards, painéis
CINZA_BORDA   = "#CBD5E1"   # bordas suaves
CINZA_TEXTO   = "#64748B"   # texto secundário
TEXTO_ESCURO  = "#1E293B"   # texto principal
VERDE_OK      = "#059669"   # status ok / desvio
VERMELHO_ERR  = "#DC2626"   # erros
LINHA_PAR     = "#F8FAFC"   # linha par da tabela
LINHA_IMPAR   = "#FFFFFF"   # linha ímpar da tabela

FONTE_MONO   = ("Consolas", 12)
FONTE_TITULO = ("Segoe UI", 22, "bold")
FONTE_NORMAL = ("Segoe UI", 13)
FONTE_SMALL  = ("Segoe UI", 11)


# ──────────────────────────────────────────────
# Widget de tabela simples (grade ScrollFrame)
# ──────────────────────────────────────────────

class TabelaResumo(ctk.CTkScrollableFrame):
    """Grade de linhas e colunas para exibir o resumo dos dados."""

    def __init__(self, master, cabecalho: list[str], linhas: list[list], **kw):
        super().__init__(master, fg_color=BRANCO, **kw)
        self._construir(cabecalho, linhas)

    def _construir(self, cabecalho, linhas):
        # Cabeçalho
        for col, texto in enumerate(cabecalho):
            ctk.CTkLabel(
                self, text=texto, font=("Segoe UI", 12, "bold"),
                text_color=AZUL_ACENTO, anchor="w",
                fg_color=AZUL_CLARO, corner_radius=0,
            ).grid(row=0, column=col, sticky="ew", padx=(0, 2), pady=(0, 2))
            self.columnconfigure(col, weight=1)

        # Linhas de dados
        for r_idx, linha in enumerate(linhas, start=1):
            bg = LINHA_PAR if r_idx % 2 == 0 else LINHA_IMPAR
            for c_idx, celula in enumerate(linha):
                ctk.CTkLabel(
                    self, text=str(celula), font=FONTE_SMALL,
                    text_color=TEXTO_ESCURO, anchor="w",
                    fg_color=bg, corner_radius=0,
                ).grid(row=r_idx, column=c_idx, sticky="ew", padx=(0, 2), pady=1)


# ──────────────────────────────────────────────
# Janela principal
# ──────────────────────────────────────────────

class AppRyzen(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Ryzen Analyzer — Análise de Dados de Pesquisa")
        self.geometry("1100x750")
        self.minsize(900, 600)
        self.configure(fg_color=CINZA_BG)

        self._df         = None
        self._resultados = None
        self._caminho    = None

        self._construir_layout()

    # ── Layout principal ──────────────────────

    def _construir_layout(self):
        self._sidebar = ctk.CTkFrame(self, width=240, fg_color=AZUL_MARINHO,
                                     corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        self._content = ctk.CTkFrame(self, fg_color=CINZA_BG, corner_radius=0)
        self._content.pack(side="right", fill="both", expand=True)

        self._montar_sidebar()
        self._montar_tela_inicial()

    def _montar_sidebar(self):
        sb = self._sidebar

        # Logo / título
        ctk.CTkLabel(sb, text="⚡ RYZEN", font=("Segoe UI", 20, "bold"),
                     text_color="#FFFFFF").pack(pady=(28, 2))
        ctk.CTkLabel(sb, text="Analyzer", font=("Segoe UI", 13),
                     text_color="#93C5FD").pack()

        ctk.CTkLabel(sb, text="─" * 28, text_color="#2D5A8E",
                     font=("Segoe UI", 10)).pack(pady=12)

        # Botão selecionar planilha
        self._btn_selecionar = ctk.CTkButton(
            sb, text="📂  Selecionar Planilha",
            font=FONTE_NORMAL, height=44,
            fg_color=AZUL_ACENTO, hover_color=AZUL_HOVER,
            text_color="#FFFFFF",
            corner_radius=10,
            command=self._selecionar_arquivo,
        )
        self._btn_selecionar.pack(padx=16, pady=6, fill="x")

        # Botão analisar
        self._btn_analisar = ctk.CTkButton(
            sb, text="🔍  Analisar Dados",
            font=FONTE_NORMAL, height=44,
            fg_color="#0F766E", hover_color="#0D6B63",
            text_color="#FFFFFF",
            corner_radius=10, state="disabled",
            command=self._iniciar_analise,
        )
        self._btn_analisar.pack(padx=16, pady=6, fill="x")

        ctk.CTkLabel(sb, text="─" * 28, text_color="#2D5A8E",
                     font=("Segoe UI", 10)).pack(pady=12)

        # Botão baixar relatório
        self._btn_relatorio = ctk.CTkButton(
            sb, text="⬇  Baixar Relatório .txt",
            font=FONTE_NORMAL, height=44,
            fg_color="#7C3AED", hover_color="#6D28D9",
            text_color="#FFFFFF",
            corner_radius=10, state="disabled",
            command=self._baixar_relatorio,
        )
        self._btn_relatorio.pack(padx=16, pady=6, fill="x")

        ctk.CTkLabel(sb, text="─" * 28, text_color="#2D5A8E",
                     font=("Segoe UI", 10)).pack(pady=12)

        self._lbl_arquivo = ctk.CTkLabel(
            sb, text="Nenhum arquivo\nselecionado.",
            font=FONTE_SMALL, text_color="#93C5FD",
            wraplength=200, justify="center",
        )
        self._lbl_arquivo.pack(padx=10)

    def _montar_tela_inicial(self):
        for w in self._content.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(self._content, fg_color="transparent")
        frame.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(frame, text="📊", font=("Segoe UI", 64)).pack()
        ctk.CTkLabel(frame, text="Ryzen Field Research Analyzer",
                     font=FONTE_TITULO, text_color=TEXTO_ESCURO).pack(pady=(8, 4))
        ctk.CTkLabel(
            frame,
            text="Selecione uma planilha Excel (.xlsx) para iniciar a análise.",
            font=FONTE_NORMAL, text_color=CINZA_TEXTO,
        ).pack()

    # ── Ações ─────────────────────────────────

    def _selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Excel", "*.xlsx *.xls"), ("Todos", "*.*")],
        )
        if not caminho:
            return

        self._caminho = caminho
        nome = os.path.basename(caminho)
        self._lbl_arquivo.configure(text=f"📄 {nome}")
        self._btn_analisar.configure(state="normal")
        self._btn_relatorio.configure(state="disabled")
        self._df = None
        self._resultados = None
        self._montar_tela_inicial()

    def _iniciar_analise(self):
        self._btn_analisar.configure(state="disabled", text="Processando...")
        self._btn_selecionar.configure(state="disabled")
        self._montar_tela_log()
        threading.Thread(target=self._executar_analise, daemon=True).start()

    def _executar_analise(self):
        try:
            df, log_carga = carregar_planilha(self._caminho)
            for msg in log_carga:
                self._append_log(msg)

            res, log_anal = analisar(df)
            for msg in log_anal:
                self._append_log(msg)

            self._df         = df
            self._resultados = res
            self.after(300, self._mostrar_resultados)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro", str(e)))
            self.after(0, self._resetar_botoes)

    def _resetar_botoes(self):
        self._btn_analisar.configure(state="normal", text="🔍  Analisar Dados")
        self._btn_selecionar.configure(state="normal")

    # ── Tela de log ───────────────────────────

    def _montar_tela_log(self):
        for w in self._content.winfo_children():
            w.destroy()

        ctk.CTkLabel(self._content, text="Processando...",
                     font=FONTE_TITULO, text_color=TEXTO_ESCURO).pack(pady=(24, 8))

        self._log_box = ctk.CTkTextbox(
            self._content, font=FONTE_MONO,
            fg_color=BRANCO, text_color=VERDE_OK,
            border_color=CINZA_BORDA, border_width=1,
            corner_radius=10, wrap="word",
        )
        self._log_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self._log_box.configure(state="disabled")

    def _append_log(self, msg: str):
        def _do():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", msg + "\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _do)

    # ── Tela de resultados ────────────────────

    def _mostrar_resultados(self):
        for w in self._content.winfo_children():
            w.destroy()

        r = self._resultados

        # Cabeçalho
        header = ctk.CTkFrame(self._content, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 8))
        ctk.CTkLabel(header, text="Resultados da Análise",
                     font=FONTE_TITULO, text_color=TEXTO_ESCURO).pack(side="left")

        # ── Linha 1 de cards ──
        cards = ctk.CTkFrame(self._content, fg_color="transparent")
        cards.pack(fill="x", padx=20, pady=4)

        metricas = [
            ("📋 Respostas",          str(r["total_respostas"])),
            ("📈 Preparo médio",      f"{r['preparo_media']} / 5"),
            ("💻 Usaria plataforma",  f"{r['plataforma_pct_sim']}%"),
            ("💼 Já estagia",         f"{r['estagio_pct_sim']}%"),
        ]
        for icone_label, valor in metricas:
            self._card(cards, icone_label, valor).pack(
                side="left", expand=True, fill="both", padx=4, pady=4)

        # ── Linha 2 de cards ──
        cards2 = ctk.CTkFrame(self._content, fg_color="transparent")
        cards2.pack(fill="x", padx=20, pady=(0, 4))

        faixa     = r.get("faixa_preco_adequada", "—")
        faixa_pct = r.get("faixa_preco_pct", 0)
        self._card(
            cards2,
            "💰 Faixa de preço mais adequada",
            f"{faixa}  ({faixa_pct}%)"
        ).pack(side="left", expand=True, fill="both", padx=4, pady=4)

        atrib         = r.get("atributo_top1", "—")
        atrib_pct     = r.get("atributo_top1_pct", 0)
        atrib_display = (atrib[:38] + "…") if len(atrib) > 40 else atrib
        self._card(
            cards2,
            "⭐ Atributo mais valorizado",
            f"{atrib_display}  ({atrib_pct}%)"
        ).pack(side="left", expand=True, fill="both", padx=4, pady=4)

        # ── Abas ──
        tabview = ctk.CTkTabview(
            self._content,
            fg_color=BRANCO,
            segmented_button_fg_color=CINZA_BG,
            segmented_button_selected_color=AZUL_ACENTO,
            segmented_button_selected_hover_color=AZUL_HOVER,
            segmented_button_unselected_color=CINZA_BG,
            segmented_button_unselected_hover_color=AZUL_CLARO,
            text_color=TEXTO_ESCURO,
            text_color_disabled=CINZA_TEXTO,
            corner_radius=10,
            border_color=CINZA_BORDA,
            border_width=1,
        )
        tabview.pack(fill="both", expand=True, padx=20, pady=(4, 16))

        abas = [
            ("Resumo Geral",      self._aba_resumo),
            ("Cursos & Períodos", self._aba_cursos),
            ("Medos",             self._aba_medos),
            ("Plataforma",        self._aba_plataforma),
            ("Preparo Técnico",   self._aba_preparo),
        ]
        for nome, construtor in abas:
            tabview.add(nome)
            construtor(tabview.tab(nome), r)

        self._btn_analisar.configure(state="normal", text="🔍  Analisar Dados")
        self._btn_selecionar.configure(state="normal")
        self._btn_relatorio.configure(state="normal")

    # ── Utilitário card ───────────────────────

    def _card(self, master, titulo, valor):
        f = ctk.CTkFrame(master, fg_color=BRANCO, corner_radius=12,
                         border_color=CINZA_BORDA, border_width=1)
        ctk.CTkLabel(f, text=titulo, font=FONTE_SMALL,
                     text_color=CINZA_TEXTO).pack(padx=16, pady=(12, 0))
        ctk.CTkLabel(f, text=valor, font=("Segoe UI", 20, "bold"),
                     text_color=AZUL_ACENTO, wraplength=300).pack(padx=16, pady=(0, 12))
        return f

    # ── Conteúdo das abas ─────────────────────

    def _aba_resumo(self, parent, r):
        cab = ["Indicador", "Valor"]
        linhas = [
            ["Total de respostas",            r["total_respostas"]],
            ["Período de coleta",             r["periodo_coleta"]],
            ["Preparo técnico médio",         f"{r['preparo_media']} / 5"],
            ["Preparo técnico mediana",       f"{r['preparo_mediana']} / 5"],
            ["Desvio padrão (preparo)",       r["preparo_desvio"]],
            ["Estudantes c/ estágio/emprego", f"{r['estagio_pct_sim']}%"],
            ["Usariam a plataforma",          f"{r['plataforma_pct_sim']}%"],
            ["Faixa de preço mais adequada",  f"{r.get('faixa_preco_adequada','—')} ({r.get('faixa_preco_pct',0)}%)"],
            ["Atributo mais valorizado",      f"{r.get('atributo_top1','—')} ({r.get('atributo_top1_pct',0)}%)"],
        ]
        TabelaResumo(parent, cab, linhas,
                     corner_radius=8).pack(fill="both", expand=True, padx=8, pady=8)

    def _aba_cursos(self, parent, r):
        total = r["total_respostas"]
        cab = ["Curso", "Respostas", "% do total"]
        linhas_c = [
            [k, v, f"{round(v/total*100,1)}%"]
            for k, v in sorted(r["cursos"].items(), key=lambda x: -x[1])
        ]
        cab_p = ["Período", "Respostas", "% do total"]
        linhas_p = [
            [k, v, f"{round(v/total*100,1)}%"]
            for k, v in sorted(r["periodos"].items(), key=lambda x: -x[1])
        ]
        ctk.CTkLabel(parent, text="Cursos", font=("Segoe UI", 13, "bold"),
                     text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(8, 2))
        TabelaResumo(parent, cab, linhas_c,
                     corner_radius=8, height=160).pack(fill="x", padx=8)
        ctk.CTkLabel(parent, text="Períodos", font=("Segoe UI", 13, "bold"),
                     text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(12, 2))
        TabelaResumo(parent, cab_p, linhas_p,
                     corner_radius=8, height=180).pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _aba_medos(self, parent, r):
        total_mencoes = sum(r["medos"].values())
        cab = ["Medo", "Menções", "% das menções"]
        linhas = [
            [k, v, f"{round(v/total_mencoes*100,1)}%"]
            for k, v in r["medos"].items()
        ]
        TabelaResumo(parent, cab, linhas,
                     corner_radius=8).pack(fill="both", expand=True, padx=8, pady=8)

    def _aba_plataforma(self, parent, r):
        total = r["total_respostas"]

        cab1 = ["Usaria a plataforma?", "Respostas", "%"]
        lin1 = [
            [k, v, f"{round(v/total*100,1)}%"]
            for k, v in r["usaria_plataforma"].items()
        ]
        cab2 = ["Investimento mensal", "Respostas", "%"]
        lin2 = [
            [k, v, f"{round(v/total*100,1)}%"]
            for k, v in sorted(r["investimento"].items(), key=lambda x: -x[1])
        ]
        cab3 = ["Funcionalidade valiosa", "Respostas", "%"]
        lin3 = [
            [k, v, f"{round(v/total*100,1)}%"]
            for k, v in sorted(r["atributos_valorizados"].items(), key=lambda x: -x[1])
        ]

        ctk.CTkLabel(parent, text="Uso da plataforma", font=("Segoe UI", 13, "bold"),
                     text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(8, 2))
        TabelaResumo(parent, cab1, lin1,
                     corner_radius=8, height=110).pack(fill="x", padx=8)

        ctk.CTkLabel(parent, text="Disposição de investimento", font=("Segoe UI", 13, "bold"),
                     text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(10, 2))
        TabelaResumo(parent, cab2, lin2,
                     corner_radius=8, height=130).pack(fill="x", padx=8)

        ctk.CTkLabel(parent, text="Funcionalidades mais valorizadas", font=("Segoe UI", 13, "bold"),
                     text_color=AZUL_ACENTO).pack(anchor="w", padx=8, pady=(10, 2))
        TabelaResumo(parent, cab3, lin3,
                     corner_radius=8).pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _aba_preparo(self, parent, r):
        total = r["total_respostas"]
        cab = ["Nota (1–5)", "Qtd. respostas", "% do total", "Barra visual"]
        max_v = max(r["preparo_dist"].values(), default=1)
        linhas = []
        for nota in sorted(r["preparo_dist"]):
            v = r["preparo_dist"][nota]
            barra = "█" * int(v * 20 / max_v)
            linhas.append([f"  {int(nota)}  ", v, f"{round(v/total*100,1)}%", barra])
        TabelaResumo(parent, cab, linhas,
                     corner_radius=8, height=220).pack(fill="x", padx=8, pady=8)

        info = ctk.CTkFrame(parent, fg_color=BRANCO, corner_radius=10,
                            border_color=CINZA_BORDA, border_width=1)
        info.pack(fill="x", padx=8, pady=4)
        stats = [
            ("Média",         r["preparo_media"]),
            ("Mediana",       r["preparo_mediana"]),
            ("Desvio padrão", r["preparo_desvio"]),
        ]
        for lbl, val in stats:
            row = ctk.CTkFrame(info, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(row, text=lbl, font=FONTE_SMALL,
                         text_color=CINZA_TEXTO).pack(side="left")
            ctk.CTkLabel(row, text=str(val), font=("Segoe UI", 13, "bold"),
                         text_color=VERDE_OK).pack(side="right")

    # ── Download .txt ─────────────────────────

    def _baixar_relatorio(self):
        if not self._resultados:
            messagebox.showwarning("Aviso", "Nenhuma análise disponível.")
            return

        dest = filedialog.asksaveasfilename(
            title="Salvar relatório",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            initialfile="relatorio_ryzen.txt",
        )
        if not dest:
            return

        try:
            gerar_relatorio(self._df, self._resultados, dest)
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{dest}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))