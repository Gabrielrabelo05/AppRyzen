"""
exec.py — Back-end: carregamento, tratamento e análise estatística dos dados.
"""

import pandas as pd
from collections import Counter
import re


# ──────────────────────────────────────────────
# Carregamento e tratamento
# ──────────────────────────────────────────────

def carregar_planilha(caminho: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Lê o Excel, formata a coluna de timestamp para DD/MM/AAAA
    e retorna (DataFrame limpo, log_de_etapas).
    """
    log = []

    log.append("📂  Lendo arquivo Excel...")
    df = pd.read_excel(caminho)
    log.append(f"✅  {len(df)} respostas e {len(df.columns)} colunas encontradas.")

    # Renomear colunas para nomes curtos e sem espaços extras
    colunas_map = {
        df.columns[0]:  "data_hora",
        df.columns[1]:  "curso",
        df.columns[2]:  "periodo",
        df.columns[3]:  "estagio",
        df.columns[4]:  "medos",
        df.columns[5]:  "suporte_univ",
        df.columns[6]:  "comunicacao",
        df.columns[7]:  "preparo_tecnico",
        df.columns[8]:  "usaria_plataforma",
        df.columns[9]:  "investimento_mensal",
        df.columns[10]: "funcionalidade_valiosa",
    }
    df = df.rename(columns=colunas_map)
    log.append("🔄  Colunas renomeadas para formato interno.")

    # Formatar data/hora → DD/MM/AAAA (padrão brasileiro)
    log.append("📅  Formatando coluna de data/hora para DD/MM/AAAA...")
    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
    df["data_hora_fmt"] = df["data_hora"].dt.strftime("%d/%m/%Y")
    nulos = df["data_hora_fmt"].isna().sum()
    if nulos:
        log.append(f"⚠️  {nulos} linha(s) com data inválida substituída(s) por '—'.")
        df["data_hora_fmt"] = df["data_hora_fmt"].fillna("—")
    log.append("✅  Datas formatadas com sucesso.")

    # Remover espaços extras de colunas texto
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].astype(str).str.strip()
    log.append("🧹  Espaços extras removidos de campos de texto.")

    return df, log


# ──────────────────────────────────────────────
# Análise estatística
# ──────────────────────────────────────────────

def analisar(df: pd.DataFrame) -> tuple[dict, list[str]]:
    """
    Gera métricas e retorna (resultados_dict, log_de_etapas).
    """
    log = []
    r = {}

    log.append("📊  Iniciando análise estatística...")

    # ── Totais gerais ──
    r["total_respostas"] = len(df)
    r["periodo_coleta"] = (
        f"{df['data_hora'].min().strftime('%d/%m/%Y')} "
        f"a {df['data_hora'].max().strftime('%d/%m/%Y')}"
    )
    log.append(f"✅  Total de respostas: {r['total_respostas']}")

    # ── Cursos ──
    r["cursos"] = df["curso"].value_counts().to_dict()
    log.append(f"🎓  Cursos identificados: {len(r['cursos'])}")

    # ── Períodos ──
    r["periodos"] = df["periodo"].value_counts().to_dict()
    log.append("🗓️  Distribuição por período calculada.")

    # ── Estágio / atuação ──
    r["estagio"] = df["estagio"].value_counts().to_dict()
    pct_sim = round(
        df["estagio"].str.lower().str.startswith("sim").sum() / len(df) * 100, 1
    )
    r["estagio_pct_sim"] = pct_sim
    log.append(f"💼  {pct_sim}% já atuam na área ou têm estágio.")

    # ── Maiores medos (múltipla escolha separada por vírgula) ──
    todos_medos = []
    for val in df["medos"].dropna():
        todos_medos.extend([m.strip() for m in val.split(",")])
    r["medos"] = dict(Counter(todos_medos).most_common())
    log.append("😰  Medos no processo seletivo contabilizados.")

    # ── Suporte da universidade ──
    r["suporte_univ"] = df["suporte_univ"].value_counts().to_dict()
    log.append("🏫  Percepção de suporte universitário calculada.")

    # ── Comunicação / apresentações ──
    r["comunicacao"] = df["comunicacao"].value_counts().to_dict()
    log.append("🎤  Segurança em comunicação calculada.")

    # ── Preparo técnico (1–5): média, mediana, desvio ──
    serie_pt = pd.to_numeric(df["preparo_tecnico"], errors="coerce").dropna()
    r["preparo_media"]   = round(float(serie_pt.mean()), 2)
    r["preparo_mediana"] = float(serie_pt.median())
    r["preparo_desvio"]  = round(float(serie_pt.std()), 2)
    r["preparo_dist"]    = serie_pt.value_counts().sort_index().to_dict()
    log.append(
        f"📈  Preparo técnico — média: {r['preparo_media']}, "
        f"mediana: {r['preparo_mediana']}, desvio: {r['preparo_desvio']}"
    )

    # ── Uso da plataforma ──
    r["usaria_plataforma"] = df["usaria_plataforma"].value_counts().to_dict()
    pct_plat = round(
        df["usaria_plataforma"].str.lower().str.startswith("sim").sum() / len(df) * 100, 1
    )
    r["plataforma_pct_sim"] = pct_plat
    log.append(f"💻  {pct_plat}% usariam a plataforma.")

    # ── Investimento mensal ──
    r["investimento"] = df["investimento_mensal"].value_counts().to_dict()
    log.append("💰  Disposição de investimento mensal calculada.")

    # ── Funcionalidade mais valiosa ──
    r["funcionalidade"] = df["funcionalidade_valiosa"].value_counts().to_dict()
    log.append("⭐  Funcionalidades mais valorizadas identificadas.")

    log.append("✅  Análise concluída com sucesso.")
    return r, log


# ──────────────────────────────────────────────
# Geração do relatório .txt
# ──────────────────────────────────────────────

def gerar_relatorio(df: pd.DataFrame, r: dict, caminho_saida: str) -> None:
    """Salva um relatório formatado em .txt."""

    sep  = "=" * 60
    sep2 = "-" * 60

    def secao(titulo):
        return f"\n{sep}\n  {titulo.upper()}\n{sep}\n"

    def item(chave, valor, indent=2):
        return f"{' ' * indent}• {chave}: {valor}\n"

    linhas = []
    linhas.append(sep)
    linhas.append("  RELATÓRIO DE ANÁLISE — PESQUISA DE CAMPO RYZEN")
    linhas.append(sep)
    linhas.append(f"\n  Período de coleta : {r.get('periodo_coleta', '—')}")
    linhas.append(f"  Total de respostas: {r.get('total_respostas', 0)}\n")

    # Cursos
    linhas.append(secao("1. Distribuição por Curso"))
    for k, v in sorted(r["cursos"].items(), key=lambda x: -x[1]):
        linhas.append(item(k, f"{v} resp. ({round(v/r['total_respostas']*100,1)}%)"))

    # Períodos
    linhas.append(secao("2. Período Atual dos Respondentes"))
    for k, v in sorted(r["periodos"].items(), key=lambda x: -x[1]):
        linhas.append(item(k, f"{v} resp. ({round(v/r['total_respostas']*100,1)}%)"))

    # Estágio
    linhas.append(secao("3. Atuação na Área / Estágio"))
    for k, v in r["estagio"].items():
        linhas.append(item(k, f"{v} resp."))
    linhas.append(f"\n  → {r['estagio_pct_sim']}% já trabalham ou têm estágio.\n")

    # Medos
    linhas.append(secao("4. Maiores Medos no Processo Seletivo"))
    for k, v in list(r["medos"].items())[:8]:
        linhas.append(item(k, f"{v} menções"))

    # Suporte universitário
    linhas.append(secao("5. Percepção de Suporte da Universidade"))
    for k, v in r["suporte_univ"].items():
        linhas.append(item(k, f"{v} resp. ({round(v/r['total_respostas']*100,1)}%)"))

    # Comunicação
    linhas.append(secao("6. Segurança em Comunicação / Apresentações"))
    for k, v in r["comunicacao"].items():
        linhas.append(item(k, f"{v} resp. ({round(v/r['total_respostas']*100,1)}%)"))

    # Preparo técnico
    linhas.append(secao("7. Preparo Técnico (Escala 1–5)"))
    linhas.append(item("Média",   r["preparo_media"]))
    linhas.append(item("Mediana", r["preparo_mediana"]))
    linhas.append(item("Desvio padrão", r["preparo_desvio"]))
    linhas.append(f"\n  Distribuição das notas:\n")
    for nota, qtd in r["preparo_dist"].items():
        barra = "█" * int(qtd * 20 / r["total_respostas"])
        linhas.append(f"    Nota {int(nota)}: {barra} {qtd}\n")

    # Plataforma
    linhas.append(secao("8. Uso da Plataforma Proposta"))
    for k, v in r["usaria_plataforma"].items():
        linhas.append(item(k, f"{v} resp."))
    linhas.append(f"\n  → {r['plataforma_pct_sim']}% usariam a plataforma.\n")

    # Investimento
    linhas.append(secao("9. Disposição de Investimento Mensal"))
    for k, v in sorted(r["investimento"].items(), key=lambda x: -x[1]):
        linhas.append(item(k, f"{v} resp. ({round(v/r['total_respostas']*100,1)}%)"))

    # Funcionalidade
    linhas.append(secao("10. Funcionalidade Mais Valiosa"))
    for k, v in sorted(r["funcionalidade"].items(), key=lambda x: -x[1]):
        linhas.append(item(k, f"{v} resp."))

    # Conclusão
    linhas.append(secao("Conclusão"))
    linhas.append(
        f"  A pesquisa coletou {r['total_respostas']} respostas de estudantes\n"
        f"  de cursos de tecnologia. Em média, os respondentes se sentem\n"
        f"  {r['preparo_media']}/5 preparados tecnicamente para o mercado.\n"
        f"  {r['plataforma_pct_sim']}% utilizariam a plataforma proposta, e\n"
        f"  {r['estagio_pct_sim']}% já atuam na área ou possuem estágio.\n"
    )
    linhas.append(sep + "\n")
    linhas.append("  Relatório gerado automaticamente pelo sistema Ryzen Analyzer.\n")
    linhas.append(sep + "\n")

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)