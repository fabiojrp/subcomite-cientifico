import json
import requests
import zipfile
import datetime
import os


class download_vacinados:
    def __init__(self):
        self.url = 'http://sgsweknow.saude.sc.gov.br/weknow/datasnap/rest/TServer/DatabaseManager_ExecuteGrid'

        self.headers = {
            'Host': 'sgsweknow.saude.sc.gov.br',
            'Connection': 'keep-alive',
            'Content-Length': '361',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Content-Type': 'text/plain',
            'Sec-GPC': '1',
            'Origin': 'http://sgsweknow.saude.sc.gov.br',
            'Referer': 'http://sgsweknow.saude.sc.gov.br/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        self.query = {"id": 16827, "linkedValues": [{"name": "ds_categoria"}, {"name": "nm_indicador"}, {"name": "nm_setor_responsavel"}], "dashboardId": 2767, "context": {
        }, "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjI2NjIyMTUsImV4cCI6MTYyMjc0ODYxNSwiYWNjb3VudElkIjoxMCwicHVibGljVmlld2VyIjp0cnVlLCJsb2dTZXNzaW9uSWQiOjM0ODMxfQ.6LIbmuRhbQx5wS2MzmRlhduB2rfIgDBgl8Yl3faBpjM"}

        print("Baixando base de dados de vacinados da DIVE...",
              end='', flush=True)

        req_DB = requests.post(
            self.url, headers=self.headers, json=self.query).text

        data_DB = json.loads(req_DB)

        print("Ok\n")

        municipios_grupos_prioritarios = data_DB['return']['rows']
        vacinados_municipios = {}

        for grupo_prioritario in municipios_grupos_prioritarios:

            if vacinados_municipios.get(grupo_prioritario['cells'][1]['value']) != None:
                vacinados_municipios[grupo_prioritario['cells']
                                     [1]['value']] = list()


if __name__ == "__main__":
    download_vacinados()
