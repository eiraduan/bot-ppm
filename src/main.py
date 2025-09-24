import download
import join_files

print("Iniciando download dos arquivos da PPM")
download.main()

print("Juntando os arquivos da PPM_RO_<ano>.xlsx no 'PPM_RO_FINAL.xlsx'")
join_files.main()