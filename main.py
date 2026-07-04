"""
===============================================================================
MÓDULO: main.py
===============================================================================

Ponto de entrada da aplicação Data Insight Copilot.

Responsável por iniciar a interface Streamlit.

===============================================================================
"""

import subprocess
import sys
from pathlib import Path


def main():
    """
    Inicia a aplicação Streamlit.
    """

    app_path = Path(__file__).parent / "app.py"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path)
        ]
    )


if __name__ == "__main__":
    main()