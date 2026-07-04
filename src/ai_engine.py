"""
===============================================================================
MÓDULO: ai_engine.py
===============================================================================

Responsável por:

- Comunicação com a LLM (Ollama)
- Construção do prompt
- Geração de insights

===============================================================================
"""

import ollama

from src.config import (
    OLLAMA_MODEL,
    OLLAMA_OPTIONS,
    DEFAULT_DATASET
)

from src.logger import setup_logger

logger = setup_logger()


# -----------------------------------------------------------------------------
# FUNÇÃO DE AUTOTESTE
# -----------------------------------------------------------------------------
def self_test():

    from src.data_loader import carregar_arquivo
    from src.profiler import gerar_profiling

    logger.info("Iniciando teste do AI Engine.")

    df = carregar_arquivo(DEFAULT_DATASET)

    perfil = gerar_profiling(df)

    resposta = gerar_insights(perfil)

    if not resposta.strip():
        raise Exception("A IA retornou uma resposta vazia.")

    print("\n" + "=" * 80)
    print("RESPOSTA DA IA")
    print("=" * 80)
    print(resposta)
    print("=" * 80)

    logger.info("AI Engine OK")

    return True


# -----------------------------------------------------------------------------
# CONSTRUÇÃO DO PROMPT
# -----------------------------------------------------------------------------
def construir_prompt(perfil: dict) -> str:
    """
    Recebe o profiling do DataFrame e monta um prompt estruturado.
    """

    logger.info("Construindo prompt para a LLM.")

    prompt = f"""
Você é um cientista de dados sênior.

Analise o seguinte conjunto de dados.

## Estrutura
- Número de linhas: {perfil['numero_de_linhas']}
- Número de colunas: {perfil['numero_de_colunas']}
- Colunas: {perfil['colunas']}
- Linhas duplicadas: {perfil['linhas_duplicadas']}
- Colunas duplicadas: {perfil['colunas_duplicadas']}

## Qualidade dos dados
- Valores nulos: {perfil['nulos']}
- Percentual de nulos: {perfil['percentual_nulos']}

## Tipos de dados
{perfil['tipos']}

## Amostra dos dados
{perfil['amostra_dados']}

## Estatísticas numéricas
{perfil['estatisticas']}

Forneça:

1. Resumo executivo.

2. Problemas reais encontrados nos dados.
Não sugira problemas hipotéticos.

3. Identifique padrões observáveis utilizando as estatísticas fornecidas.

4. Destaque possíveis outliers, valores mínimos e máximos relevantes.

5. Recomendações de negócio baseadas nos dados apresentados.

6. Sempre indique se cada conclusão é:
- Baseada nos dados
- Inferência
"""

    return prompt


# -----------------------------------------------------------------------------
# CONSULTA À LLM
# -----------------------------------------------------------------------------
def perguntar_llm(prompt: str) -> str:
    """
    Envia um prompt para a LLM e garante que o modelo
    seja descarregado da memória ao final.
    """

    logger.info("Enviando prompt ao Ollama.")

    try:

        resposta = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options=OLLAMA_OPTIONS
        )

        logger.info("Resposta recebida da LLM.")

        return resposta["message"]["content"]

    finally:

        logger.info("Descarregando modelo da memória.")

        ollama.chat(
            model=OLLAMA_MODEL,
            messages=[],
            keep_alive=0
        )

        logger.info("Modelo descarregado.")


# -----------------------------------------------------------------------------
# FUNÇÃO PÚBLICA
# -----------------------------------------------------------------------------
def gerar_insights(perfil: dict) -> str:
    """
    Recebe o profiling do DataFrame e retorna os insights da IA.
    """

    prompt = construir_prompt(perfil)

    return perguntar_llm(prompt)


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    self_test()