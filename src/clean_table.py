import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

def main():
    # --- Carrega as variáveis de ambiente do arquivo .env ---
    load_dotenv()

    # --- Configurações do Banco de Dados usando variáveis de ambiente ---
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    try:
        print("Tentando estabelecer a conexão com o banco de dados...")
        conexao = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Conexão estabelecida com sucesso!")
        
        cursor = conexao.cursor()

        # --- Criação da Tabela (com verificação para evitar erros) ---
        print("Verificando e criando a tabela 'dados_ppm' se ela não existir...")
        
        # Adiciona a verificação "IF NOT EXISTS" para evitar erros se a tabela já existir
        clean_table = """
        TRUNCATE TABLE gisdb.gisadmin.dados_ppm RESTART IDENTITY;
        DROP TABLE gisdb.gisadmin.dados_ppm_mapa;
        """
        cursor.execute(clean_table)
        
        conexao.commit()
        print("Tabela 'dados_ppm' TRUNCATE com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if 'conexao' in locals() and conexao:
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()