# tests/test_runner.py

# Importa importlib para carregar módulos dinamicamente pelo nome.
import importlib
# Importa traceback para formatar o rastreamento de exceções em texto legível.
import traceback
# Importa datetime para recuperar a data e a hora atuais.
from datetime import datetime
# Importa Path para manipular caminhos de arquivo de forma independente de plataforma.
from pathlib import Path

# Lista dos módulos do projeto que serão testados.
MODULOS = [
    "src.config",
    "src.data_loader",
    "src.profiler",
    "src.charts",
    "src.ai_engine",
    "src.logger"
]

def executar_testes():

    # Lista que irá conter as linhas do relatório de resultados.
    resultado = []

    # Cabeçalho do relatório, com separadores e data/hora.
    resultado.append("=" * 60)
    resultado.append("DATA INSIGHT COPILOT - SELF TEST")
    resultado.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    resultado.append("=" * 60)
    resultado.append("")

    for nome_modulo in MODULOS:

        try:

            # Importa o módulo dinamicamente.
            modulo = importlib.import_module(nome_modulo)

            # Se o módulo possui uma função self_test, executa-a.
            if hasattr(modulo, "self_test"):

                if modulo.self_test() is False:
                    
                    raise Exception("Self Test retornou False.")

            # Registra o sucesso do módulo no relatório.
            resultado.append(f"[OK] {nome_modulo}")

        except Exception as erro:

            # Registra o erro com o nome do módulo.
            resultado.append(f"[ERRO] {nome_modulo}")
            resultado.append("")

            # Adiciona o traceback completo ao relatório.
            resultado.append(traceback.format_exc())

            # Separa os blocos de erro no relatório.
            resultado.append("-" * 60)

    # Define o caminho de saída do relatório.

    caminho = Path("tests/relatorio_teste.txt")
    
    #caso a pasta tests não exista, o script a criará automaticamente.
    caminho.parent.mkdir(
    parents=True,
    exist_ok=True
)

    # Abre o arquivo em modo de escrita com codificação UTF-8.
    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        # Grava todas as linhas do relatório separadas por nova linha.
        arquivo.write("\n".join(resultado))

    # Exibe o caminho do arquivo gerado no console.
    print(f"Relatório salvo em: {caminho}")


if __name__ == "__main__":

    executar_testes()