# ⚡ Ryzen Field Research Analyzer

Ferramenta desktop para análise automática de dados de pesquisa de campo, exportada do Google Forms em formato Excel (`.xlsx`).

---

## 📋 Pré-requisitos

- **Python 3.10+** (recomendado: 3.11 ou 3.12)
  - Download: https://www.python.org/downloads/
  - ⚠️ Durante a instalação, marque a opção **"Add Python to PATH"**

---

## 📁 Estrutura de arquivos

```
analise/
├── main.py          # Ponto de entrada — execute este arquivo
├── interface.py     # Interface gráfica (CustomTkinter)
├── exec.py          # Lógica de análise e geração de relatório
└── README.md
```

---

## 🚀 Como rodar

### 1. Instalar dependências

Abra o terminal (CMD ou PowerShell) na pasta do projeto e execute:

```bash
pip install customtkinter pandas openpyxl
```

### 2. Executar o programa

```bash
python main.py
```

> O próprio `main.py` verifica se as dependências estão instaladas e avisa caso alguma esteja faltando.

---

## 🖥️ Como usar

1. Clique em **📂 Selecionar Planilha** e escolha o arquivo `.xlsx` exportado do Google Forms
2. Clique em **🔍 Analisar Dados** — o sistema processa automaticamente
3. Navegue pelas abas para ver os resultados:
   - **Resumo Geral** — visão consolidada de todos os indicadores
   - **Cursos & Períodos** — distribuição por curso e semestre
   - **Medos** — ranking dos medos mais citados
   - **Plataforma** — uso, investimento e funcionalidades valorizadas
   - **Preparo Técnico** — distribuição de notas com estatísticas
4. Clique em **⬇ Baixar Relatório .txt** para exportar o relatório completo

---

## 📊 O que é analisado

| Métrica | Descrição |
|---|---|
| Total de respostas | Quantidade de linhas válidas na planilha |
| Preparo técnico | Média, mediana e desvio padrão das notas (1–5) |
| % que já estagia | Percentual de respostas "Sim" na coluna de estágio |
| % que usaria a plataforma | Percentual de interesse na plataforma |
| Faixa de preço adequada | Valor de investimento mais citado (moda) |
| Atributo mais valorizado | Funcionalidade mais mencionada nas respostas |
| Medos | Ranking de medos (respostas de múltipla escolha) |
| Cursos e períodos | Distribuição dos respondentes por curso e semestre |

---

## 📄 Colunas esperadas na planilha

A planilha deve conter colunas com nomes similares a:

| Coluna esperada | Exemplo de dado |
|---|---|
| `curso` | Engenharia de Software |
| `periodo` | 5º período |
| `preparo_tecnico` | 3 |
| `estagio` | Sim / Não |
| `usaria_plataforma` | Sim / Não |
| `investimento_mensal` | R$ 30 a R$ 50 |
| `funcionalidade_valiosa` | Desafios reais, Mentoria |
| `medos` | Falta de tempo, Dificuldade técnica |

> O sistema faz mapeamento automático de colunas — nomes aproximados são aceitos.

---

## ⚠️ Possíveis erros

| Erro | Solução |
|---|---|
| `ModuleNotFoundError` | Execute `pip install customtkinter pandas openpyxl` |
| `KeyboardInterrupt` ao fechar | Normal no Windows com Python 3.14 — não afeta o funcionamento |
| Planilha não carrega | Verifique se o arquivo é `.xlsx` e não está aberto no Excel |
| Colunas não encontradas | Verifique se os nomes das colunas batem com o esperado |

---

## 🛠️ Tecnologias utilizadas

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — interface gráfica moderna
- [Pandas](https://pandas.pydata.org/) — análise e manipulação de dados
- [OpenPyXL](https://openpyxl.readthedocs.io/) — leitura de arquivos Excel

---

## 👤 Autor

Projeto desenvolvido para análise de pesquisa de campo — **Ryzen**.
