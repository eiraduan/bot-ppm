import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import logging 
from log_utils import setup_logging

def main():
    # --- Carrega as variáveis de ambiente do arquivo .env ---
    load_dotenv()

    setup_logging('clean_table.log')

    # --- Configurações do Banco de Dados usando variáveis de ambiente ---
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    try:
        logging.info("Tentando estabelecer a conexão com o banco de dados...")
        conexao = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        logging.info("Conexão estabelecida com sucesso!")
        
        cursor = conexao.cursor()

        # --- Criação da Tabela (com verificação para evitar erros) ---
        logging.info("Verificando e criando a tabela 'dados_ppm' se ela não existir...")
        
        # Adiciona a verificação "IF NOT EXISTS" para evitar erros se a tabela já existir
        clean_table = """
        TRUNCATE TABLE gisdb.gisadmin.dados_ppm RESTART IDENTITY;
        DROP TABLE gisdb.gisadmin.dados_ppm_mapa;
        """
        cursor.execute(clean_table)
        
        conexao.commit()
        logging.info("Tabela 'dados_ppm' TRUNCATE com sucesso.")

    except Exception as e:
        logging.error(f"Erro: {e}")

    finally:
        if 'conexao' in locals() and conexao:
            cursor.close()
            conexao.close()
            logging.info("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()