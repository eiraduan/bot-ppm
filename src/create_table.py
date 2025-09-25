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
        print("Verificando e criando a tabela 'dados_ppm_efetivo_rebanhos' se ela não existir...")
        
        # Adiciona a verificação "IF NOT EXISTS" para evitar erros se a tabela já existir
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dados_ppm_efetivo_rebanhos (
            id SERIAL PRIMARY KEY,
            nivel_territorial_codigo INTEGER,
            nivel_territorial VARCHAR(255),
            unidade_de_medida_codigo INTEGER,
            unidade_de_medida VARCHAR(255),
            valor INTEGER,
            municipio_codigo INTEGER, 
            municipio VARCHAR(255),
            ano_codigo INTEGER,
            ano INTEGER,
            variavel_codigo INTEGER,
            variavel VARCHAR(255),
            tipo_rebanho_codigo INTEGER,
            tipo_rebanho VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        
        conexao.commit()
        print("Tabela 'dados_ppm_efetivo_rebanhos' verificada/criada com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if 'conexao' in locals() and conexao:
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()