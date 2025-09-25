import download
import clean_table
import create_table_map
import insert
import join_files

print("Iniciando download dos arquivos da PPM")
download.main()

print("Juntando os arquivos da PPM_RO_<ano>.xlsx no 'PPM_RO_FINAL.xlsx'")
join_files.main()

print("Limpando a tabela da 'dados_ppm' e apagando a tabela 'dados_ppm_mapa'")
clean_table.main()

print("Inserindo dados na tabela 'dados_ppm'")
insert.main()

print("Criando a tabela do mapa da pam 'dados_ppm_mapa'")
create_table_map.main()

