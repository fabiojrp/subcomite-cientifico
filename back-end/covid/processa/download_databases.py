import urllib.request
import json
import requests
#from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib
import zipfile


class download_databases:
    def __init__(self):
        self.url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral'

        self.headers = {
            'authority': 'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)',
            'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm',
            'origin': 'https://covid.saude.gov.br',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://covid.saude.gov.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        req_DB = requests.get(self.url, headers=self.headers).text

        data_DB = json.loads(req_DB)
        filename = data_DB['results'][0]['texto_rodape'][:-14]+'.zip'
        # print(filename)
        print("Baixando base de dados do Ministério da Saúde ...",
              end='', flush=True)
        url_zip = requests.get(data_DB['results'][0]['arquivo']['url'])

        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall("Dados_MS")
        # with open(filename, 'wb') as s:
        #     s.write(url_zip.content)

        print('Ok\n')
