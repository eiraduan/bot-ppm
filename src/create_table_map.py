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
        print("Verificando e criando a tabela 'dados_ppm_mapa' se ela não existir...")
        
        # Adiciona a verificação "IF NOT EXISTS" para evitar erros se a tabela já existir
        create_table_query = """
        CREATE TABLE gisadmin.dados_ppm_mapa AS
        SELECT
            dp.nivel_territorial_codigo,
            dp.nivel_territorial,
            dp.unidade_de_medida_codigo,
            dp.unidade_de_medida,
            dp.valor,
            dp.municipio_codigo,
            dp.municipio,
            dp.ano_codigo,
            dp.ano,
            dp.variavel_codigo,
            dp.variavel,
            dp.tipo_rebanho_codigo,
            dp.tipo_rebanho,
            rm.nm_mun,
            rm.shape AS geom
        FROM
            gisadmin.dados_ppm AS dp
        INNER JOIN
            gisadmin.ro_municipios_2022 AS rm
        ON
            CAST(dp.municipio_codigo AS VARCHAR) = rm.cd_mun;

        ALTER TABLE gisadmin.dados_ppm_mapa ADD COLUMN id SERIAL PRIMARY KEY;
        """

        cursor.execute(create_table_query)
        
        conexao.commit()
        print("Tabela 'dados_ppm_mapa' verificada/criada com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if 'conexao' in locals() and conexao:
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()