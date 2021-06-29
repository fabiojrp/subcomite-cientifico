import pandas as pd
import json
import requests
import datetime
import os
import psycopg2

from datetime import date
from datetime import datetime
from io import StringIO
from sqlalchemy import create_engine
from pandas import ExcelWriter
from urllib.parse import quote
from covid.processa.dados.tabelas import Tabelas
# from dados.tabelas import Tabelas


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
            'Pessoas de 50 a 54 anos': 27,
            'Trabalhadores da Limpeza Urbana e Manejo de Resíduos Sólidos': 28,
            'Pessoas de 55 a 59 anos': 29,
            'Gestantes e puérperas - Comorbidades': 30,
            'Reservado 3': 31,
            'Reservado 4': 32,
            'Reservado 5': 33,
            'Reservado 6': 34,
            'Reservado 7': 35,
        }

        with open(os.getcwd() + '/back-end/covid/processa/vacinas/municipios.txt') as f:
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

        req_accessToken = requests.post("http://sgsweknow.saude.sc.gov.br:80/weknow/datasnap/rest/TSecurityApi/AuthenticateAsPublicViewer",
                                        headers=self.headers, json={"accountToken": "{68AE9BAF-B5AE-4548-8681-1DCA3E838F66}"}).text
        data_token = json.loads(req_accessToken)
        if (data_token['success'] != True):
            print(data_token)
            return

        self.query = {"id": 16827,
                      "linkedValues": [{"name": "ds_categoria"}, {"name": "nm_indicador"}, {"name": "nm_setor_responsavel"}],
                      "dashboardId": 2767, "context": {},
                      "accessToken": data_token['accessToken']}

        print("Baixando base de dados de vacinados da DIVE...",
              end='', flush=True)

        req_DB = requests.post(
            self.url, headers=self.headers, json=self.query).text

        data_DB = json.loads(req_DB)
        if 'error' in data_DB:
            print("Erro!!!\n")
            if (data_DB['error']):
                print(data_DB['error'])
                return 0
            else:
                raise Exception(data_DB['errorMessage']['title'] +
                                ": " + data_DB['errorMessage']['text'])

        # with open('dados '+date.today().strftime("%Y-%m-%d")+'.json', 'w') as outfile:
        #     json.dump(data_DB, outfile)

        print(" Ok")
        return data_DB

    def getFileLocal(self, file):
        with open('/Users/marcelocendron/Dropbox/web/subcomite/' + file) as f:
            data_DB = json.load(f)

        return data_DB

    def processData(self, data_DB, dataValor=0):
        tabelas = Tabelas()
        print("Processando dados dos municípios...",
              end='', flush=True)

        municipios_grupos_prioritarios = data_DB['return']['rows']
        dadosGeral = []
        for grupo_prioritario in municipios_grupos_prioritarios:
            try:
                # Substitui os nomes dos municípios pelo código do IBGE
                municipio = self.listaMunicipios[grupo_prioritario['cells'][0]['value'].upper(
                ).strip()]
            except KeyError as k:
                raise Exception("Município não encontrado:" +
                                grupo_prioritario['cells'][0]['value'])

            # try:
            #     grupo = self.listaGrupos[grupo_prioritario['cells'][3]['value']]
            # except KeyError as k:
            #     raise Exception("Grupo não encontrado:" +
            #                     grupo_prioritario['cells'][3]['value'])

            # data = datetime.strptime(
            #     grupo_prioritario['cells'][9]['value'], '%Y-%m-%d').date()
            if dataValor != 0:
                data = datetime.strptime(dataValor, '%Y-%m-%d').date()
            else:
                data = pd.to_datetime(
                    datetime.now().strftime("%Y-%m-%d")).date()

            dadosMunicipio = {
                'Municipio': municipio,
                'regional': tabelas.getRegionalMunicipioBrasil(municipio),
                'Data': data,
                'Grupo': grupo_prioritario['cells'][3]['value'],
                'Popul.categ.': grupo_prioritario['cells'][4]['value'],
                'D1': grupo_prioritario['cells'][5]['value'],
                'D2': grupo_prioritario['cells'][6]['value']
            }
            dadosGeral.append(dadosMunicipio)
        # print(vacinados_municipios)
        df = pd.DataFrame(dadosGeral)

        #  converte todos os valores para números
        # df['Grupo'] = df['Grupo'].apply(pd.to_numeric)
        # df['Popul.categ.'] = df['Popul.categ.'].apply(pd.to_numeric)
        df['D1'] = df['D1'].apply(pd.to_numeric)
        df['D2'] = df['D2'].apply(pd.to_numeric)

        # df = pd.DataFrame(data=vacinados_municipios, index=vacinados_municipios.keys(), columns=pd.MultiIndex.from_tuples(
        #     ))
        print(" Ok")
        return df

    def storeExcel(self, df):
        print("Salvando os dados no excel...", end='', flush=True)
        tabelas = Tabelas()

        with open(os.getcwd() + '/back-end/covid/processa/vacinas/municipios.txt') as f:
            dadosMunicipio = f.read()
        # Reconstruindo a lista dos munícipios.
        municipios_rev = dict(
            map(reversed, json.loads(dadosMunicipio).items()))

        # listaGrupos_rev = dict(
        #     map(reversed,  self.listaGrupos.items()))

        regionais_rev = dict(
            map(reversed,  tabelas.regional.items()))

        # Busca na listas os munícipios e substitui de volta pelos valores
        df['Municipio'] = df['Municipio'].replace(municipios_rev)
        # df['Grupo'] = df['Grupo'].replace(listaGrupos_rev)
        df['regional'] = df['regional'].replace(regionais_rev)

        df_regional = self.insertPercent(df, ['regional', 'Data'])
        df_municipios = self.insertPercent(df, ['Municipio', 'Data'])

        df_educa = df[df['Grupo'] == 'Trabalhadores da Educação']
        df_regional_educa = self.insertPercent(df_educa, ['regional', 'Data'])
        df_municipios_educa = self.insertPercent(
            df_educa, ['Municipio', 'Data'])

        df_regional_educa2 = self.insertPercent(
            df_regional_educa, ['regional'])

        with ExcelWriter('dados.xlsx') as writer:
            df_regional_educa2.to_excel(
                writer, sheet_name='Percentual_educacao')
            df.to_excel(writer, sheet_name='dados')
            df_regional.to_excel(writer, sheet_name='regionais')
            df_municipios.to_excel(writer, sheet_name='municipios')
            df_regional_educa.to_excel(writer, sheet_name='regionais_educacao')
            df_municipios_educa.to_excel(
                writer, sheet_name='municipios_educacao')

        print(" Ok")

    def insertPercent(self, df, dataColumns):
        # Corrigir soma da população

        df2 = df.groupby(dataColumns,  as_index=False)[
            ['D1', 'D2']].sum()
        # df2['Percentual_D1'] = df2['D1'] / \
        #     df2['Popul.categ.']
        # df2['Percentual_D2'] = df2['D2'] / \
        #     df2['Popul.categ.']
        return df2

    def connect(self):
        try:
            conn = psycopg2.connect(**self.param_dic)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn

    def storeBD(self, df, table='vacinacao_dive'):
        # df = df.groupby(['Municipio', 'regional'],  as_index=False)[
        #     ['D1', 'D2']].sum()
        df['data_cadastro'] = pd.to_datetime(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        print("Salvando os dados... ", end='', flush=True)
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
            if_exists='append'
            # if_exists='replace'
        )
        print(" Ok.")

        # conn = self.connect()
        # print("Salvando os dados... ", end='', flush=True)
        # # save dataframe to an in memory buffer
        # buffer = StringIO()
        # df.to_csv(buffer, index_label=False, index=False, header=False)
        # buffer.seek(0)

        # cursor = self.conn.cursor()
        # try:
        #     cursor.copy_from(buffer, table, sep=",")
        #     self.conn.commit()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print("Error: %s" % error)
        #     self.conn.rollback()
        #     cursor.close()
        #     return 1

        # print("Ok")
        # cursor.close()


if __name__ == "__main__":

    dv = download_vacinados()

    dataDB = dv.getFile()
    df = dv.processData(dataDB)
    dv.storeBD(df)

    # dataDB = dv.getFileLocal('dados-11-06.json')
    # df = dv.processData(dataDB, '2021-06-11')
    # dv.storeBD(df)

    # dataDB = dv.getFileLocal('dados-17-06.json')
    # df = dv.processData(dataDB, '2021-06-17')
    # dv.storeBD(df)

    # dataDB = dv.getFileLocal('dados-18-06.json')
    # df = dv.processData(dataDB, '2021-06-18')
    # dv.storeBD(df)

    dv.storeExcel(df)
