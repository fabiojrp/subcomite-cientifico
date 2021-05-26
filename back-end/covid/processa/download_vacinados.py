import json
import requests
import zipfile
import datetime
import os


class download_vacinados:
    def __init__(self):
        self.parcialUrl = 'http://www.dive.sc.gov.br/notas-tecnicas/docs/Balan%C3%A7o%20'

        self.dateFile = datetime.datetime.today().strftime("%d.%m.%Y")

        self.headers = {
            'Host': 'www.dive.sc.gov.br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-GPC': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '71ee7fdec80999ced2eb8fdaf35f0f64=7na6vqi21sp6e0ral9rqh9b3h7; _ga=GA1.4.1476828240.1621800443; _gid=GA1.4.221078845.1622039019',
            'Range': 'bytes=1010064-1010064',
            'If-Range': '620f12-5c2b5ef2633e2'
        }

        self.url = self.parcialUrl + str(self.dateFile) + str('.zip')

        print("Baixando base de dados de vacinados...",
              end='', flush=True)

        req_DB = requests.get(self.url, headers=self.headers)

        print("Ok\n")

        filename = 'Balanço ' + \
            str(self.dateFile)+'.zip'
        # os.replace(filename, 'vacinados.zip')

        with open(filename, 'wb') as s:
            s.write(req_DB.content)

        print("Descompactando o arquivo ...",
              end='', flush=True)
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall("vacinados")

        print('Ok\n')


teste = download_vacinados()
