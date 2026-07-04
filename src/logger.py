''''
## `logger.py`

Logs do sistema.

Mesmo padrão que usamos no Mail Insight Agent.
'''

"""
===============================================================================
MÓDULO: logger.py
===============================================================================

Responsável pela configuração do sistema de logs da aplicação.

Todos os módulos devem utilizar este logger para registrar eventos,
avisos e erros.

===============================================================================
"""

import logging

from src.config import LOG_DIR, LOG_FILE, LOG_LEVEL


# -----------------------------------------------------------------------------
# FUNÇÃO DE AUTOTESTE
# -----------------------------------------------------------------------------
def self_test():

    logger = setup_logger()

    logger.info("Teste de log executado com sucesso.")

    print("Logger OK")

    return True


# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DO LOGGER
# -----------------------------------------------------------------------------
def setup_logger():

    # Garante que a pasta de logs exista
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("DataInsightCopilot")

    # Evita adicionar handlers duplicados
    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL))

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Log em arquivo
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    # Log no terminal
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    self_test()