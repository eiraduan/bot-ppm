import pandas as pd
from pathlib import Path
import logging
import sys

# Importa a função de configuração de log do novo módulo
from log_utils import setup_logging

def juntar_arquivos_excel(pasta_origem: Path):
    """
    Lê todos os arquivos .xlsx em uma pasta, os concatena em um único DataFrame
    e salva o resultado em um novo arquivo, substituindo o antigo se existir.

    Args:
        pasta_origem (Path): O objeto Path da pasta com os arquivos Excel.
    """
    logger = logging.getLogger(__name__)

    # 1. Define o caminho do arquivo de saída
    nome_arquivo_saida = "PPM_RO_FINAL.xlsx"
    caminho_completo_saida = pasta_origem / nome_arquivo_saida
    
    # 2. Verifica se o arquivo final existe e o apaga para evitar duplicações
    if caminho_completo_saida.exists():
        logger.info(f"Arquivo '{nome_arquivo_saida}' existente. Apagando...")
        caminho_completo_saida.unlink()
    
    logger.info(f"Buscando arquivos na pasta: {pasta_origem}")
    
    lista_de_dataframes = []

    # Encontra todos os arquivos .xlsx que começam com "PPM_RO_"
    # A verificação 'if arquivo.name != nome_arquivo_saida' garante que
    # o arquivo de saída (se por algum motivo não for apagado) não será lido.
    arquivos_excel = sorted([
        arquivo for arquivo in pasta_origem.glob("PPM_RO_*.xlsx") 
        if arquivo.name != nome_arquivo_saida
    ])

    if not arquivos_excel:
        logger.error("Não foram encontrados arquivos .xlsx para serem unidos.")
        return

    # Itera sobre cada arquivo e lê o conteúdo para um DataFrame
    for arquivo in arquivos_excel:
        logger.info(f"Lendo arquivo: {arquivo.name}")
        try:
            df_temp = pd.read_excel(arquivo)
            lista_de_dataframes.append(df_temp)
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo {arquivo.name}: {e}")
            continue

    # Concatena todos os DataFrames da lista em um só
    df_final = pd.concat(lista_de_dataframes, ignore_index=True)

    # 3. Salva o novo DataFrame no arquivo
    df_final.to_excel(caminho_completo_saida, index=False)

    logger.info("Processo de união concluído com sucesso!")
    logger.info(f"Todos os dados foram salvos no arquivo: {caminho_completo_saida}")
    logger.info(f"O DataFrame final possui {len(df_final)} linhas.")

def main():
    """
    Função principal para executar a união dos arquivos.
    """
    # A configuração do logging é chamada aqui, passando o nome do arquivo de log
    setup_logging('join_files.log')
    
    diretorio_script = Path(__file__).parent
    pasta_origem_dados = diretorio_script.parent / "files"
    
    juntar_arquivos_excel(pasta_origem_dados)

# --- Ponto de entrada do script ---
if __name__ == "__main__":
    main()