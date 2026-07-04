'''
===============================================================================
MÓDULO: profiler.py
===============================================================================

Responsável por realizar o diagnóstico inicial de um DataFrame.

Principais informações geradas:
- Quantidade de linhas
- Quantidade de colunas
- Valores nulos
- Linhas duplicadas
- Colunas duplicadas
- Tipos de dados
- Estatísticas descritivas

Esse módulo é normalmente utilizado na etapa de análise exploratória
e validação da qualidade dos dados.
===============================================================================
'''

#%%
# Marcador utilizado por IDEs como VS Code e Spyder para dividir células.

# IMPORTAÇÃO DE BIBLIOTECAS
import pandas as pd

# Importa a função responsável por carregar arquivos para um DataFrame.
from src.data_loader import carregar_arquivo
from src.config import DEFAULT_DATASET
from src.logger import setup_logger

logger = setup_logger()
# -----------------------------------------------------------------------------
# FUNÇÃO DE AUTOTESTE DO MÓDULO
# -----------------------------------------------------------------------------
# Executa um teste simples para verificar se o profiler está funcionando.
def self_test():

    # Carrega o dataset de exemplo.
    df = carregar_arquivo(DEFAULT_DATASET)

    # Gera o profiling do dataset carregado.
    resultado = gerar_profiling(df)

    # Verifica se o dataset possui registros.
    # Caso não possua, lança uma exceção.
    if resultado["numero_de_linhas"] == 0:
        raise Exception("Dataset vazio")

    # Mensagem indicando sucesso do teste.
    logger.info("Profiler OK")

    # Retorna True para indicar que o teste passou.
    return True


# -----------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL DE PROFILING
# -----------------------------------------------------------------------------
# Recebe um DataFrame e gera um dicionário contendo diversas métricas.
def gerar_profiling(df):

    logger.info("Iniciando geração do profiling.")
    
    # Cria um dicionário contendo informações estruturadas do dataset.
    resultado = {

        # Quantidade total de linhas.
        "numero_de_linhas": df.shape[0],

        # Quantidade total de colunas.
        "numero_de_colunas": df.shape[1],

        # Quantidade de linhas duplicadas.
        "linhas_duplicadas": int(df.duplicated().sum()),

        # Quantidade de colunas duplicadas.
        # O DataFrame é transposto para que as colunas possam ser comparadas.
        "colunas_duplicadas": int(df.T.duplicated().sum()),

        # Quantidade de valores nulos por coluna.
        "nulos": df.isnull().sum().to_dict(),

        # Percentual de valores nulos por coluna.
        # mean() calcula a proporção de nulos.
        # Multiplica por 100 para obter percentual.
        # round(2) limita a duas casas decimais.
        "percentual_nulos":
            (df.isnull().mean()*100).round(2).to_dict(),

        # Tipos de dados de cada coluna.
        "tipos":
            df.dtypes.astype(str).to_dict(),

        # Lista contendo os nomes das colunas.
        "colunas":
            list(df.columns),

        # Estatísticas descritivas das colunas numéricas.
        # Inclui métricas como:
        # count, mean, std, min, 25%, 50%, 75% e max.
        "estatisticas":
            df.describe().round(2),
            
            
        "amostra_dados":
            df.head(5).to_dict(orient="records")

    }
    
    logger.info("Profiling gerado com sucesso.")
    
    # Retorna o dicionário contendo todo o diagnóstico.
    return resultado


# -----------------------------------------------------------------------------
# FUNÇÃO DE EXIBIÇÃO DO PROFILING
# -----------------------------------------------------------------------------
# Recebe o dicionário gerado por gerar_profiling() e imprime as informações.
def exibir_profiling(resultado):

    # Exibe cabeçalho visual.
    print("\n" + "="*100)
    print("📊 PERFIL DO DATASET")
    print("="*100)

    # Exibe informações gerais.
    print(f"Linhas: {resultado['numero_de_linhas']}\n")
    print(f"Numero de Colunas: {resultado['numero_de_colunas']}\n")
    print(f"Colunas: {resultado['colunas']}\n")
    print(f"Linhas duplicadas: {resultado['linhas_duplicadas']}\n")
    print(f"Colunas duplicadas: {resultado['colunas_duplicadas']}\n")

    # -------------------------------------------------------------------------
    # EXIBIÇÃO DOS VALORES NULOS
    # -------------------------------------------------------------------------
    print("\nValores Nulos")

    # Percorre todas as colunas e exibe a quantidade de nulos.
    for coluna, valor in resultado["nulos"].items():

        print(f"{coluna}: {valor}")

    # -------------------------------------------------------------------------
    # EXIBIÇÃO DOS PERCENTUAIS DE NULOS
    # -------------------------------------------------------------------------
    print("\nPercentual de Nulos")

    # Percorre todas as colunas e exibe o percentual de nulos.
    for coluna, valor in resultado["percentual_nulos"].items():

        print(f"{coluna}: {valor}%")

    # -------------------------------------------------------------------------
    # EXIBIÇÃO DOS TIPOS DE DADOS
    # -------------------------------------------------------------------------
    print("\nTipos")

    # Percorre todas as colunas e exibe o dtype correspondente.
    for coluna, tipo in resultado["tipos"].items():

        print(f"{coluna}: {tipo}")

    # -------------------------------------------------------------------------
    # EXIBIÇÃO DAS ESTATÍSTICAS DESCRITIVAS
    # -------------------------------------------------------------------------
    print("\nEstatísticas:")

    # Percorre cada coluna presente nas estatísticas.
    for coluna, valores in resultado["estatisticas"].items():

        print(f"\n{coluna}")

        # Percorre cada métrica estatística da coluna.
        for metrica, valor in valores.items():

            print(f"  {metrica}: {valor}")

    # -------------------------------------------------------------------------
    # EXIBIÇÃO DOS DADOS
    # -------------------------------------------------------------------------

    print("\nAmostra dos Dados")

    for linha in resultado["amostra_dados"]:

        print(linha)


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA DO SCRIPT
# -----------------------------------------------------------------------------
# Este bloco será executado apenas quando o arquivo for executado diretamente.
# Não será executado quando o módulo for importado.
if __name__ == "__main__":

    # Carrega o dataset.
    df = carregar_arquivo(
        r"data\AI_Impact_on_Jobs_2030.csv"
    )

    # Gera o profiling.
    profiling_result = gerar_profiling(df)

    # Exibe o resultado na tela.
    exibir_profiling(profiling_result)

# %%
# Marcador de célula para IDEs.