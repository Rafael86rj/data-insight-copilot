'''
## `config.py`

Configurações gerais:

* modelo Ollama
* título app
* cores
* limites
'''
#função de teste do molulo
def self_test():

    # Verifica se os diretórios foram resolvidos corretamente
    assert BASE_DIR.exists(), "BASE_DIR não encontrado."

    assert DATA_DIR.parent.exists(), "Diretório pai de DATA_DIR inexistente."

    assert OUTPUT_DIR.parent.exists(), "Diretório pai de OUTPUT_DIR inexistente."

    # Verifica se o modelo foi definido
    assert isinstance(OLLAMA_MODEL, str), "OLLAMA_MODEL inválido."

    # Verifica se as opções do Ollama são um dicionário
    assert isinstance(OLLAMA_OPTIONS, dict), "OLLAMA_OPTIONS inválido."

    print("Config OK")

    return True

"""
===============================================================================
MÓDULO: config.py
===============================================================================

Centraliza todas as configurações utilizadas pelo projeto.

Alterando este arquivo é possível modificar o comportamento da aplicação
sem alterar os demais módulos.

===============================================================================
"""

from pathlib import Path

# =============================================================================
# CAMINHOS DO PROJETO
# =============================================================================

# Pasta raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Pasta onde ficam os datasets
DATA_DIR = BASE_DIR / "data"

# Pasta de saída
OUTPUT_DIR = BASE_DIR / "output"

# Pasta de logs
LOG_DIR = BASE_DIR / "logs"

# =============================================================================
# DATASET PADRÃO
# =============================================================================

DEFAULT_DATASET = DATA_DIR / "AI_Impact_on_Jobs_2030.csv"

# =============================================================================
# CONFIGURAÇÕES DO OLLAMA
# =============================================================================

OLLAMA_MODEL = "qwen2.5:3b"

OLLAMA_OPTIONS = {
    "temperature": 0.2,
    "num_predict": 500
}

# =============================================================================
# CONFIGURAÇÕES DO STREAMLIT
# =============================================================================

APP_TITLE = "Data Insight Copilot"

APP_ICON = "📊"

APP_LAYOUT = "wide"

# =============================================================================
# CONFIGURAÇÕES DE LOG
# =============================================================================

LOG_FILE = LOG_DIR / "data_insight.log"

LOG_LEVEL = "INFO"

if __name__ == "__main__":

    self_test()