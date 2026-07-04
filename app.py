'''
## `app.py`

Será o ponto de entrada do Streamlit.

Equivalente ao `main.py` do projeto anterior.

É ele que roda o dashboard.

---
'''
"""
===============================================================================
MÓDULO: app.py
===============================================================================

Interface principal do Data Insight Copilot.

Responsável por integrar:

- Upload de arquivos
- Profiling
- Visualizações
- IA

===============================================================================
"""

import streamlit as st

from src.config import (
    APP_TITLE,
    APP_ICON,
    APP_LAYOUT,
    DEFAULT_DATASET
)

from src.logger import setup_logger

from src.data_loader import carregar_arquivo
from src.profiler import gerar_profiling

from src.charts import (
    grafico_nulos,
    grafico_tipos,
    grafico_distribuicao_numerica,
    grafico_categorico
)
from src.ai_engine import gerar_insights
# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
)

logger = setup_logger()

logger.info("Aplicação iniciada.")
# -----------------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------------

if "df" not in st.session_state:
    st.session_state.df = None

if "profiling" not in st.session_state:
    st.session_state.profiling = None

if "insights" not in st.session_state:
    st.session_state.insights = None   
    
# -----------------------------------------------------------------------------
# TÍTULO
# -----------------------------------------------------------------------------

st.title("📊 Data Insight Copilot")

st.markdown(
    """
Ferramenta para análise exploratória de dados utilizando Python,
Plotly e Inteligência Artificial.
"""
)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------

st.sidebar.title("Configurações")

arquivo = st.sidebar.file_uploader(

    "Selecione um CSV ou Excel",

    type=["csv", "xlsx"]

)

usar_dataset = st.sidebar.button(

    "Usar Dataset de Exemplo"

)

analisar = st.sidebar.button(

    "Analisar Dados"

)


df = st.session_state.df
profiling = st.session_state.profiling
insights = st.session_state.insights


if analisar:

    if profiling is None:

        st.sidebar.warning(
            "Carregue um dataset primeiro."
        )

    else:

        with st.spinner(
            "A IA está analisando o dataset..."
        ):

            logger.info("Gerando insights da IA.")

            insights = gerar_insights(profiling)

            st.session_state.insights = insights
            
            insights = st.session_state.insights

            logger.info("Insights gerados.")

if usar_dataset:

    logger.info("Carregando dataset padrão.")

    df = carregar_arquivo(DEFAULT_DATASET)

    profiling = gerar_profiling(df)

    st.session_state.df = df
    st.session_state.profiling = profiling

    # limpa insights antigos
    st.session_state.insights = None
    insights = None

    st.sidebar.success("Dataset carregado com sucesso.")


# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------

aba1, aba2, aba3, aba4 = st.tabs(

    [

        "📊 Visão Geral",

        "📋 Profiling",

        "📈 Visualizações",

        "🤖 IA"

    ]

)

# -----------------------------------------------------------------------------
# ABA 1
# -----------------------------------------------------------------------------

with aba1:

    st.header("📊 Visão Geral")

    if profiling is not None:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Linhas",
            profiling["numero_de_linhas"]
        )

        col2.metric(
            "Colunas",
            profiling["numero_de_colunas"]
        )

        col3.metric(
            "Linhas Duplicadas",
            profiling["linhas_duplicadas"]
        )

        col4.metric(
            "Colunas Duplicadas",
            profiling["colunas_duplicadas"]
        )

        st.subheader("Amostra dos Dados")

        st.dataframe(df.head())

    else:

        st.info("Aguardando análise...")

# -----------------------------------------------------------------------------
# ABA 2
# -----------------------------------------------------------------------------

with aba2:

    st.header("📋 Profiling")

    if profiling is not None:

        st.subheader("Tipos de Dados")

        st.json(profiling["tipos"])

        st.subheader("Valores Nulos")

        st.json(profiling["nulos"])

        st.subheader("Percentual de Nulos")

        st.json(profiling["percentual_nulos"])

        st.subheader("Estatísticas")

        st.dataframe(profiling["estatisticas"])

    else:

        st.info("Aguardando análise...")

# -----------------------------------------------------------------------------
# ABA 3
# -----------------------------------------------------------------------------

with aba3:

    st.header("📈 Visualizações")

    if df is not None:

        st.subheader("Valores Nulos")

        st.plotly_chart(
            grafico_nulos(df),
            use_container_width=True
        )

        st.subheader("Tipos de Dados")

        st.plotly_chart(
            grafico_tipos(df),
            use_container_width=True
        )

        st.subheader("Distribuição Numérica")

        colunas_numericas = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if colunas_numericas:

            coluna = st.selectbox(

                "Selecione uma coluna numérica",

                colunas_numericas

            )

            st.plotly_chart(

                grafico_distribuicao_numerica(
                    df,
                    coluna
                ),

                use_container_width=True

            )

        st.subheader("Distribuição Categórica")

        colunas_categoricas = df.select_dtypes(
            include="object"
        ).columns.tolist()

        if colunas_categoricas:

            coluna = st.selectbox(

                "Selecione uma coluna categórica",

                colunas_categoricas,

                key="categoria"

            )

            st.plotly_chart(

                grafico_categorico(
                    df,
                    coluna
                ),

                use_container_width=True

            )

    else:

        st.info("Aguardando análise...")

# -----------------------------------------------------------------------------
# ABA 4
# -----------------------------------------------------------------------------

with aba4:

    st.header("🤖 Insights da IA")

    if insights is not None:

        st.markdown(insights)

        st.download_button(

            "📥 Baixar Relatório",

            data=insights,

            file_name="insights.txt",

            mime="text/plain"

        )

    else:

        st.info(

            "Clique em 'Analisar Dados' para gerar os insights."

        )
# -----------------------------------------------------------------------------
# RODAPÉ
# -----------------------------------------------------------------------------

st.divider()

st.caption("Data Insight Copilot • Python • Streamlit • Plotly • Ollama")