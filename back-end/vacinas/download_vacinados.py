import pandas as pd
from pandas import ExcelWriter
import json
import requests
import zipfile
import datetime
import os
import numpy as np
from datetime import datetime
import psycopg2
from io import StringIO
from sqlalchemy import create_engine
from urllib.parse import quote


class download_vacinados:
    def __init__(self):
        self.listaGrupos = {
            'Gestantes e puéperas - Comorbidades': 1,
            'Comorbidades': 2,
            'Caminhoneiros': 3,
            'Trabalhadores industriais': 4,
            'Trabalhadores portuários': 5,
            'Trabalhadores de transporte aéreo': 6,
            'Trabalhos de transporte metroviário e ferroviário': 7,
            'Trabalhos de transporte coletivo rodoviário': 8,
            'Força de Seg. e Salv., Seg. Prisional, For. Armadas e GM': 9,
            'Trabalhadores da Educação': 10,
            'População privada de liberdade': 11,
            'Funcionários do sistema de privação de liberdade': 12,
            'Pessoa em situação de rua': 13,
            'População 18 a 59 anos - Deficiência Permanente Grave': 14,
            'Povos e Comunidades Tradicionais Quilombola': 15,
            'Pessoas de 60 a 64 anos': 16,
            'Pessoas de 65 a 69 anos': 17,
            'Pessoas de 70 a 74 anos': 18,
            'Pessoas de 75 a 79 anos': 19,
            'Pessoas de 80 a 84 anos': 20,
            'Pessoas de 85 a 89 anos': 21,
            'Pessoas de 90 anos ou mais': 22,
            'Povos Indígenas Vivendo em Terras Indígenas': 23,
            'Pessoas deficientes institucionalizadas': 24,
            'Pessoas idosas institucionalizadas': 25,
            'Trabalhadores da Saúde': 26,
            'Reservado 1': 27,
            'Reservado 2': 28,
            'Reservado 3': 29,
            'Reservado 4': 30,
        }

        with open(os.getcwd() + '/back-end/vacinas/municipios.txt') as f:
            dadosMunicipio = f.read().upper()
        # Reconstruindo a lista dos munícipios.
        self.listaMunicipios = json.loads(dadosMunicipio)

        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "!admpasswd@covid"
        }

        # self.db = self.connect(self.param_dic)

    def getFile(self):
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
        if 'error' in data_DB:
            print("Erro!!!\n")
            raise Exception(data_DB['errorMessage']['title'] +
                            ": " + data_DB['errorMessage']['text'])

        print(" Ok")
        return data_DB

    def processData(self, data_DB):
        print("Processando dados dos municípios...",
              end='', flush=True)

        municipios_grupos_prioritarios = data_DB['return']['rows']
        dadosGeral = []
        for grupo_prioritario in municipios_grupos_prioritarios:
            try:
                municipio = self.listaMunicipios[grupo_prioritario['cells'][0]['value'].upper(
                ).strip()]
            except KeyError as k:
                print("Município não encontrado:" +
                      grupo_prioritario['cells'][0]['value'])

            try:
                grupo = self.listaGrupos[grupo_prioritario['cells'][3]['value']]
            except KeyError as k:
                raise("Grupo não encontrado:" +
                      grupo_prioritario['cells'][3]['value'])

            data = datetime.strptime(
                grupo_prioritario['cells'][9]['value'], '%Y-%m-%d').date()
            dadosMunicipio = {
                'Municipio': municipio,
                'Data': data,
                'Grupo': grupo,
                'Popul.categ.': grupo_prioritario['cells'][4]['value'],
                'D1': grupo_prioritario['cells'][5]['value'],
                'D2': grupo_prioritario['cells'][6]['value']
            }
            dadosGeral.append(dadosMunicipio)
        # print(vacinados_municipios)
        df = pd.DataFrame(dadosGeral)

        #  converte todos os valores para números
        df['Grupo'] = df['Grupo'].apply(pd.to_numeric)
        df['Popul.categ.'] = df['Popul.categ.'].apply(pd.to_numeric)
        df['D1'] = df['D1'].apply(pd.to_numeric)
        df['D2'] = df['D2'].apply(pd.to_numeric)

        # df = pd.DataFrame(data=vacinados_municipios, index=vacinados_municipios.keys(), columns=pd.MultiIndex.from_tuples(
        #     ))
        print(" Ok")
        return df

    def storeExcel(self, df):

        #  with ExcelWriter('dados.xlsx') as writer:
        #     df.to_excel(writer, sheet_name='df')
        #     df.filter(regex='D1', axis=1).to_excel(writer, sheet_name='D1')
        #     df.filter(regex='D2', axis=1).to_excel(writer, sheet_name='D2')
        print("Ok..")

    def connect(self, params_dic):
        try:
            conn = psycopg2.connect(**params_dic)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn

    def storeBD(self, df, table='vacinacao_dive'):
        print("Cria a tabela se não existe...", end='', flush=True)
        connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            self.param_dic['user'],
            quote(self.param_dic['password']),
            self.param_dic['host'],
            self.param_dic['database']
        )
        engine = create_engine(connect)
        df.to_sql(
            table,
            con=engine,
            index=False,
            # if_exists='append'
            if_exists='replace'
        )
        print(" Ok.")

        print("Salvando os dados...", end='', flush=True)
        # save dataframe to an in memory buffer
        buffer = StringIO()
        df.to_csv(buffer, index_label=False, index=False, header=False)
        buffer.seek(0)

        cursor = self.conn.cursor()
        try:
            cursor.copy_from(buffer, table, sep=",")
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1

        print("Ok.")
        cursor.close()


if __name__ == "__main__":
    dv = download_vacinados()
    dataDB = dv.getFile()
    df = dv.processData(dataDB)
    dv.storeExcel()
    # dv.storeBD(df)
