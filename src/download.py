import sidrapy
import datetime
from pathlib import Path
import logging 

log_pasta = Path('logs')
log_pasta.mkdir(exist_ok=True)
log_arquivos = log_pasta / 'app.log'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_arquivos), logging.StreamHandler()])

def main():
    date_now = datetime.datetime.now().year
    first_year = 2019
    diretorio_script = Path(__file__).parent
    diretorio_projeto = diretorio_script.parent

    pasta_dados = diretorio_projeto / "files"
    pasta_dados.mkdir(parents=True, exist_ok=True)
    print(f"Pasta de dados criada ou já existente em: {pasta_dados}")
    print("Iniciando o processo de download de arquivos anuais da Pesquisa da Pecuária Municipal (PPM)")

    codigos_municipios_ro = [
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

    municipios_str = ",".join(codigos_municipios_ro)

    for year in range(first_year, date_now):
        try:
            dados_sidra = sidrapy.get_table(
            table_code="3939",
            territorial_level="6",
            ibge_territorial_code=municipios_str,
            period=f"{year}",
            variable="all",
            classifications={"79": "2670,2675,2672,32794,32795,2681,2677,32796,32793,2680"}
            )

            nome_arquivos = f"PMM_RO_{year}.xlsx"
            caminho_completo = pasta_dados / nome_arquivos
            dados_sidra.columns = dados_sidra.iloc[0]
            dados_sidra = dados_sidra.iloc[1:,]
            dados_sidra.to_excel(caminho_completo, index=False)

            print(f"Arquivo 'PPM_RO_{year}.xlsx' gerado com sucesso!")
            logging.info(f"Arquivo 'PPM_RO_{year}.xlsx' gerado com sucesso!")
        
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o arquivo Excel: {e}")
            logging.error(f"Ocorreu um erro ao gerar o arquivo Excel: {e}")
            
if __name__ == '__main__':
    main()