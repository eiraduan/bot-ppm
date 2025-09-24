import logging
import sys
from pathlib import Path

def setup_logging(log_file_name: str):
    """
    Configura o sistema de logging do projeto, criando um arquivo de log
    com o nome especificado.

    Args:
        log_file_name (str): O nome do arquivo de log, como 'join_files.log'.
    """
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / log_file_name

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
