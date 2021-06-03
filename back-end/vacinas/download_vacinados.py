import pandas as pd
from pandas import ExcelWriter
import json
import requests
import zipfile
import datetime
import os
import numpy as np


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
        }, "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjI3NTUyNTAsImV4cCI6MTYyMjg0MTY1MCwiYWNjb3VudElkIjoxMCwicHVibGljVmlld2VyIjp0cnVlLCJsb2dTZXNzaW9uSWQiOjM2MzY0fQ.xiq26V_FFNW3tFA1xDVt3rtkURm-hSXRCCrjsqptCpM"}

        print("Baixando base de dados de vacinados da DIVE...",
              end='', flush=True)

        req_DB = requests.post(
            self.url, headers=self.headers, json=self.query).text

        data_DB = json.loads(req_DB)

        df = pd.read_json(req_DB)

        print("Ok\n")

        # df = pd.read_json(req_DB)
        # with ExcelWriter('dados.xlsx') as writer:
        #     df.to_excel(writer, sheet_name='df')
        if 'error' in data_DB:
            raise Exception(data_DB['errorMessage']['title'] +
                            ": " + data_DB['errorMessage']['text'])

        municipios_grupos_prioritarios = data_DB['return']['rows']
        vacinados_municipios = {}
        dados = []

        for grupo_prioritario in municipios_grupos_prioritarios:
            municipio = grupo_prioritario['cells'][0]['value']
            grupo = grupo_prioritario['cells'][3]['value']

            if vacinados_municipios.get(municipio) == None:
                vacinados_municipios[municipio] = {
                    # 'regional': tabelas.getRegionalMunicipioBrasil(codigo_ibge_municipio),
                    # 'populacao': Utils.convert_to_int(value['populacaoTCU2019']),
                    'Gestantes e puéperas - Comorbidades': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Comorbidades': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Caminhoneiros': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhadores industriais': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhadores portuários': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhadores de transporte aéreo': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhos de transporte metroviário e ferroviário': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhos de transporte coletivo rodoviário': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Força de Seg. e Salv., Seg. Prisional, For. Armadas e GM': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhadores da Educação': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'População privada de liberdade': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Funcionários do sistema de privação de liberdade': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoa em situação de rua': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'População 18 a 59 anos - Deficiência Permanente Grave': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Povos e Comunidades Tradicionais Quilombola': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 60 a 64 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 65 a 69 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 70 a 74 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 75 a 79 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 80 a 84 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 85 a 89 anos': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas de 90 anos ou mais': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Povos Indígenas Vivendo em Terras Indígenas': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas deficientes institucionalizadas': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Pessoas idosas institucionalizadas': {'Popul.categ.': -1, 'D1': -1, 'D2': -1},
                    'Trabalhadores da Saúde': {'Popul.categ.': -1, 'D1': -1, 'D2': -1}
                }
            try:
                vacinados_municipios[municipio][grupo]['Popul.categ.'] = grupo_prioritario['cells'][4]['value']
                vacinados_municipios[municipio][grupo]['D1'] = grupo_prioritario['cells'][5]['value']
                vacinados_municipios[municipio][grupo]['D2'] = grupo_prioritario['cells'][6]['value']
                d = zip(grupo_prioritario['cells'][4]['value'], grupo_prioritario['cells']
                        [5]['value'], grupo_prioritario['cells'][6]['value'])
                dados.append(
                    list(vacinados_municipios[municipio][grupo].values()))
            except Exception as mensagem:
                print("Erro: " + mensagem)

        grupos = np.array(list(vacinados_municipios[municipio].keys()))
        categorias = np.array(
            list(vacinados_municipios[municipio][grupo].keys()))

        # print(vacinados_municipios)

        df = pd.DataFrame(data=vacinados_municipios, index=vacinados_municipios.keys(), columns=pd.MultiIndex.from_tuples(
            zip(grupos, categorias)))

        print("a")


if __name__ == "__main__":
    download_vacinados()
