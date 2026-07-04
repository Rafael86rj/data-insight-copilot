'''
===============================================================================
MÓDULO: data_loader.py
===============================================================================

Responsável pela aquisição e carregamento de datasets.

Funcionalidades principais:
- Download de datasets do Kaggle
- Cópia dos arquivos para a pasta local do projeto
- Carregamento de arquivos CSV
- Carregamento de arquivos XLSX
- Validação de formatos suportados

Este módulo centraliza toda a lógica de entrada de dados da aplicação.
===============================================================================
'''

# -----------------------------------------------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# -----------------------------------------------------------------------------

# Biblioteca para manipulação de diretórios e caminhos de arquivos.
import os

# Biblioteca para copiar arquivos preservando metadados.
import shutil

# Biblioteca utilizada para download de datasets do Kaggle.
import kagglehub

# Biblioteca principal para manipulação de dados tabulares.
import pandas as pd


from src.config import DATA_DIR

from src.logger import setup_logger

logger = setup_logger()


DATA_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# FUNÇÃO DE AUTOTESTE DO MÓDULO
# -----------------------------------------------------------------------------
# Executa uma validação simples para garantir que:
# 1. O download do dataset funciona.
# 2. Arquivos foram encontrados.
# 3. O carregamento dos dados funciona.
# 4. O DataFrame resultante não está vazio.
def self_test():

    print("Testando data_loader")

    # Realiza download do dataset e retorna os arquivos encontrados.
    arquivos = baixar_dataset_kaggle()

    # Verifica se algum arquivo foi obtido.
    if len(arquivos) == 0:
        raise Exception("Nenhum arquivo encontrado")

    # Carrega o primeiro arquivo disponível.
    df = carregar_arquivo(arquivos[0])

    # Verifica se o DataFrame contém registros.
    if df.empty:
        raise Exception("DataFrame vazio")

    # Mensagem indicando sucesso do teste.
    print("Data Loader OK")

    # Retorna True para indicar que o teste passou.
    return True


# -----------------------------------------------------------------------------
# FUNÇÃO DE DOWNLOAD DO DATASET
# -----------------------------------------------------------------------------
# Faz o download do dataset hospedado no Kaggle e copia os arquivos
# para a pasta local "data".
def baixar_dataset_kaggle():
    logger.info("Iniciando download do dataset do Kaggle.")
    # Realiza download do dataset utilizando o identificador do Kaggle.
    dataset_path = kagglehub.dataset_download(
        "muhammadwaqas023/ai-impact-in-future-on-jobs-market-in-2030"
    )

    # Lista que armazenará os caminhos dos arquivos encontrados.
    arquivos = []

    # Cria a pasta "data" caso ela ainda não exista.
    os.makedirs("data", exist_ok=True)

    # Percorre todos os arquivos presentes no diretório baixado.
    for arquivo in os.listdir(dataset_path):

        # Caminho completo do arquivo original.
        origem = os.path.join(dataset_path, arquivo)

        # Caminho de destino dentro da pasta local do projeto.
        destino = DATA_DIR / arquivo

        # Verifica se o arquivo já existe na pasta destino.
        if os.path.exists(destino):

            # Evita cópia desnecessária.
            logger.info(f"Arquivo já existe: {arquivo}")

            # Adiciona o arquivo à lista de retorno.
            arquivos.append(destino)

            # Passa para o próximo arquivo.
            continue

        # Copia o arquivo preservando metadados.
        shutil.copy2(origem, destino)

        # Exibe mensagem de sucesso.
        logger.info(f"Arquivo copiado: {arquivo}")

        logger.info(f"{len(arquivos)} arquivo(s) disponível(is) para uso.")
        
        # Adiciona o arquivo copiado à lista.
        arquivos.append(destino)
        
    
    # Retorna todos os caminhos encontrados.
    return arquivos


# -----------------------------------------------------------------------------
# FUNÇÃO DE CARREGAMENTO DE ARQUIVOS
# -----------------------------------------------------------------------------
# Recebe o caminho de um arquivo e realiza a leitura de acordo com sua
# extensão.
def carregar_arquivo(caminho):

    # Extrai a extensão do arquivo e converte para minúsculo.
    # Exemplo:
    # "dados.csv" -> ".csv"
    # "planilha.xlsx" -> ".xlsx"
    extensao = os.path.splitext(caminho)[1].lower()

    # -------------------------------------------------------------------------
    # LEITURA DE ARQUIVOS CSV
    # -------------------------------------------------------------------------
    if extensao == ".csv":

        # Retorna um DataFrame carregado a partir do CSV.
        return pd.read_csv(caminho)

    # -------------------------------------------------------------------------
    # LEITURA DE ARQUIVOS EXCEL
    # -------------------------------------------------------------------------
    elif extensao == ".xlsx":

        # Retorna um DataFrame carregado a partir do Excel.
        return pd.read_excel(caminho)

    # -------------------------------------------------------------------------
    # FORMATO NÃO SUPORTADO
    # -------------------------------------------------------------------------
    else:

        # Lança exceção informando a extensão inválida.
        raise ValueError(
            f"Formato não suportado: {extensao}"
        )



# -----------------------------------------------------------------------------
# PONTO DE ENTRADA DO SCRIPT
# -----------------------------------------------------------------------------
# Este bloco será executado apenas quando o arquivo for executado
# diretamente.
#
# Não será executado quando este módulo for importado por outro arquivo.
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Faz download dos arquivos do dataset.
    arquivos = baixar_dataset_kaggle()

    # Exibe os arquivos encontrados.
    print("\nArquivos encontrados:")

    # Percorre a lista de arquivos retornada.
    for arquivo in arquivos:
        print(arquivo)

    # Carrega o primeiro arquivo disponível.
    df = carregar_arquivo(arquivos[0])

    # Exibe uma prévia dos dados.
    print("\nPrévia do Dataset:")

    # Mostra as cinco primeiras linhas do DataFrame.
    print(df.head())