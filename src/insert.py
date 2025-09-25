import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import logging 

def main():
# Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    logger = logging.getLogger(__name__)

    # --- Configurações do Banco de Dados (usando variáveis de ambiente) ---
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    # O segundo argumento de .getenv é o valor padrão
    DB_PORT = os.getenv("DB_PORT", 5432)

    # --- Configurações do Processamento ---
    # Define o diretório onde o script está
    DIRETORIO_SCRIPT = Path(__file__).parent
    # Sobe um nível para o diretório raiz do projeto e desce para a pasta 'files'
    PASTA_ARQUIVOS = DIRETORIO_SCRIPT.parent / "files"

    # Define o nome da tabela de destino no banco de dados
    TABELA_DESTINO = "dados_ppm"

    logger.info("Iniciando o processo de ETL (Extrair, Transformar, Carregar)...")


    # 1. Configura a conexão com o PostgreSQL
    try:
        url_object = URL.create(
            "postgresql+psycopg2",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        engine = create_engine(url_object)
        logger.info("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        # Encerra o script em caso de erro fatal de conexão
        exit()

    # 2. Processa o arquivo consolidado
    arquivo_consolidado = PASTA_ARQUIVOS / "PPM_RO_FINAL.xlsx"

    if not arquivo_consolidado.exists():
        logger.info(f"Erro: O arquivo '{arquivo_consolidado.name}' não foi encontrado na pasta '{PASTA_ARQUIVOS}'.")
    else:
        try:
            logger.info(f"Processando o arquivo: {arquivo_consolidado.name}")
            
            # Lê o arquivo Excel completo para um DataFrame do pandas
            df = pd.read_excel(arquivo_consolidado)
            
            # 3. Transformação (ajustado para os dados do PAM)
            # Limpa os nomes das colunas, removendo a primeira linha que é o cabeçalho
            # df.columns = df.iloc[0]
            #df = df[1:].copy()

            # Renomeia colunas para o padrão do banco de dados (minúsculas)
            df.rename(columns={
                "Nível Territorial (Código)": "nivel_territorial_codigo",
                "Nível Territorial": "nivel_territorial",
                "Unidade de Medida (Código)": "unidade_de_medida_codigo",
                "Unidade de Medida": "unidade_de_medida",
                "Valor": "valor",
                "Município (Código)": "municipio_codigo",
                "Município": "municipio",
                "Ano (Código)": "ano_codigo",
                "Ano": "ano",
                "Variável (Código)": "variavel_codigo",
                "Variável": "variavel",
                "Tipo de rebanho (Código)": "tipo_rebanho_codigo",
                "Tipo de rebanho": "tipo_rebanho"
            }, inplace=True)

            df['valor'] = df['valor'].replace({'-','..','...'}, pd.NA)

            # Adicione aqui outras transformações necessárias para os dados do PAM
            # Por exemplo, conversão de tipos, limpeza de valores, etc.

            if not df.empty:
                logger.info(f"{len(df)} linhas prontas para serem carregadas.")
                
                # 4. Salva os dados no banco de dados
                df.to_sql(
                    name=TABELA_DESTINO,
                    con=engine,
                    if_exists='append', # Adiciona os dados à tabela existente
                    index=False # Não salva o índice do DataFrame como uma coluna
                )
                logger.info(f"Dados do arquivo '{arquivo_consolidado.name}' salvos na tabela '{TABELA_DESTINO}' com sucesso.")
            else:
                logger.info(f"Nenhuma linha encontrada no arquivo {arquivo_consolidado.name}.")
                
        except Exception as e:
            logger.error(f"Erro ao processar o arquivo {arquivo_consolidado.name}: {e}")

    logger.info("Processamento finalizado.")

if __name__ == "__main__":
    main()