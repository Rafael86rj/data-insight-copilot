'''
## `charts.py`

Vai gerar os gráficos automáticos.

'''
import plotly.express as px

from src.logger import setup_logger

logger = setup_logger()

def self_test():
    from src.data_loader import carregar_arquivo

    df = carregar_arquivo(r"data\AI_Impact_on_Jobs_2030.csv")

    fig = grafico_nulos(df)

    if fig is None:
        raise Exception("Falha ao gerar gráfico.")

    logger.info("Charts OK")
    return True

# src/charts.py

def grafico_nulos(df):
    nulos = df.isnull().sum()

    fig = px.bar(
        x=nulos.index,
        y=nulos.values,
        labels={"x": "Coluna", "y": "Quantidade de nulos"},
        title="Quantidade de valores nulos por coluna",
        text=nulos.values #coloar rotulo
        
    )
    logger.info("Gerando gráfico de valores nulos.")
    return fig


def grafico_tipos(df):
    tipos = df.dtypes.astype(str).value_counts()

    fig = px.bar(
        x=tipos.index,
        y=tipos.values,
        labels={"x": "Tipo de dado", "y": "Quantidade de colunas"},
        title="Distribuição dos tipos de dados",
        text=tipos.values
    )
    logger.info("Gerando gráfico de tipos.")
    return fig

def grafico_distribuicao_numerica(df, coluna):

    if coluna not in df.columns:
        raise ValueError(f"Coluna '{coluna}' não encontrada.")

    fig = px.histogram(
        df,
        x=coluna,
        nbins=20,
        title=f"Distribuição de {coluna}",
        labels={"x": coluna, "y": "Quantidade"},
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Valores",
        yaxis_title="Quantidade"
    )

    return fig

def grafico_categorico(df, coluna, top_n=10):
    contagem = df[coluna].value_counts().head(top_n)

    fig = px.bar(
        x=contagem.index,
        y=contagem.values,
        labels={"x": coluna, "y": "Quantidade"},
        title=f"Top {top_n} valores de {coluna}",
        text=contagem.values
    )
    logger.info(f"Gerando gráfico categórico: {coluna}")
    return fig

def testar_todos_os_graficos():
    from src.data_loader import carregar_arquivo

    df = carregar_arquivo(r"data\AI_Impact_on_Jobs_2030.csv")

    grafico_nulos(df).show()
    grafico_tipos(df).show()
    grafico_distribuicao_numerica(df, "Years_Experience").show()
    grafico_categorico(df, "Industry").show()
#função de teste do molulo
if __name__ == "__main__":
    testar_todos_os_graficos()