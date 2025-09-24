import sidrapy
import datetime
from pathlib import Path

def main():
    date_now = datetime.datetime.now().year
    first_year = 2019
    diretorio_script = Path(__file__).parent
    diretorio_projeto = diretorio_script.parent

    pasta_dados = diretorio_projeto / "files"
    pasta_dados.mkdir(parents=True, exist_ok=True)
    print(f"Pasta de dados criada ou já existente em: {pasta_dados}")
    print("Iniciando o processo de download de arquivos anuais da Pesquisa da Pecuária Municipal (PPM)")
    
if __name__ == '__main__':
    main()