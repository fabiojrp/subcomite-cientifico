# ftp://boavista:dados_abertos@ftp2.ciasc.gov.br/boavista_covid_dados_abertos.csv
from ftplib import FTP
import ftplib

nomeArquivo = "boavista_covid_dados_abertos.csv"

with FTP(host='ftp2.ciasc.gov.br', user='boavista', passwd='dados_abertos') as ftp:
    tamanhoArquivo = 0;
    
    ftp.sendcmd('TYPE I') 
    tamanhoArquivo = int(ftp.size(nomeArquivo))/(1024*1024)

    print(f"Tamanho do arquivo: {tamanhoArquivo:.2f} MB", flush=True)
    
    with open(nomeArquivo, 'wb') as local_file:
        ftp.retrbinary('RETR ' + nomeArquivo, local_file.write)

    ftp.quit()
 