import sidrapy
import datetime
from pathlib import Path
import logging
import pandas as pd
import sys

def setup_logging():
    """Configura o sistema de logging para o projeto."""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'download.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """
    Função principal para baixar dados da Pesquisa da Pecuária Municipal (PPM)
    e salvá-los em arquivos Excel por ano.
    """
    # Configura o sistema de logging
    setup_logging()
    
    # Obtém o ano atual e define o ano inicial para a coleta
    current_year = datetime.datetime.now().year
    first_year = 2019
    
    # Define os caminhos do diretório do projeto e da pasta de dados
    project_dir = Path(__file__).resolve().parent.parent
    print(project_dir)
    data_dir = project_dir / "files"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Pasta de dados criada ou já existente em: {data_dir}")
    logging.info("Iniciando o processo de download de arquivos anuais da Pesquisa da Pecuária Municipal (PPM)")
    
    # Códigos de municípios do estado de Rondônia (RO)
    municipality_codes_ro = [
        "1100106", "1100205", "1100015", "1100023", "1100049", "1100056",
        "1100064", "1100080", "1100098", "1100114", "1100122", "1100155",
        "1100189", "1100254", "1100288", "1100304", "1100320", "1100338",
        "1100130", "1100148", "1100296", "1100346", "1100031", "1100379",
        "1100452", "1100924", "1100940", "1101435", "1101450", "1101468",
        "1101476", "1101484", "1101492", "1101559", "1101757", "1100072",
        "1100262", "1100403", "1100502", "1100601", "1100700", "1100809",
        "1100908", "1101005", "1101104", "1101203", "1101302", "1101401",
        "1101500", "1101609", "1101708", "1101807"
    ]
    
    # Converte a lista de códigos para uma string separada por vírgula
    municipalities_str = ",".join(municipality_codes_ro)
    
    # Loop para baixar dados anuais, começando do ano inicial até o ano atual
    for year in range(first_year, current_year + 1):
        try:
            logging.info(f"Iniciando download para o ano: {year}")
            
            # Baixa os dados da tabela 3939 do SIDRA (IBGE)
            sidra_data = sidrapy.get_table(
                table_code="3939",
                territorial_level="6",
                ibge_territorial_code=municipalities_str,
                period=f"{year}",
                variable="all",
                classifications={"79": "2670,2675,2672,32794,32795,2681,2677,32796,32793,2680"}
            )
            
            # Converte os dados para um DataFrame do pandas
            df = pd.DataFrame(sidra_data)

            # Define a primeira linha como cabeçalho e remove-a
            df.columns = df.iloc[0]
            df = df.iloc[1:, :]

            # Define o caminho completo para o arquivo de saída
            file_name = f"PPM_RO_{year}.xlsx"
            full_path = data_dir / file_name
            
            # Salva o DataFrame em um arquivo Excel
            df.to_excel(full_path, index=False)
            
            logging.info(f"Arquivo '{file_name}' gerado com sucesso em: {full_path}")
            
        except Exception as e:
            logging.error(f"Ocorreu um erro ao gerar o arquivo Excel para o ano {year}: {e}")

if __name__ == '__main__':
    main()