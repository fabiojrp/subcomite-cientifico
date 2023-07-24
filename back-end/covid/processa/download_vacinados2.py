# importa bibliotecas e seus derivados modulos
import json
import requests
import pandas as pd
# import pprint
import os

# importa especificos modulos
# from xml.dom import minidom
from datetime import datetime

# from io import StringIO
from sqlalchemy import create_engine
from urllib.parse import quote

# from covid.processa.dados.tabelas import Tabelas
from covid.processa.dados.tabelas import Tabelas


class download_vacinados2:
    def __init__(self, simulacao=0):
        self.tabelas = Tabelas()
        self.dataAtualizacao = datetime.now()
        
        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "xxxx"
        }
        
        with open(os.getcwd() + '/covid/processa/vacinas/municipios.txt') as f:
            self.dadosMunicipio = f.read().upper()
        # Reconstruindo a lista dos munícipios.
        self.municipios = json.loads(self.dadosMunicipio)

        # site: https://app.powerbi.com/view?r=eyJrIjoiOTM2Y2Y1M2QtMjcxNC00ZGRmLTk0NzEtZjIyNWQxOTQ2MWIxIiwidCI6ImExN2QwM2ZjLTRiYWMtNGI2OC1iZDY4LWUzOTYzYTJlYzRlNiJ9
        # Aba 8
        # link da aba: https://app.powerbi.com/view?r=eyJrIjoiOTM2Y2Y1M2QtMjcxNC00ZGRmLTk0NzEtZjIyNWQxOTQ2MWIxIiwidCI6ImExN2QwM2ZjLTRiYWMtNGI2OC1iZDY4LWUzOTYzYTJlYzRlNiJ9&pageName=ReportSectioncb5f966e3459abaf6ab9

        self.url = 'https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true'
        
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'wabi-brazil-south-api.analysis.windows.net',
            'Origin': 'https://app.powerbi.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Referer': 'https://app.powerbi.com/',
            'Content-Length': '3314',
            'Connection': 'keep-alive',
            # 'X-PowerBI-ResourceKey': '0cd771d0-47f0-4b51-bf82-6b97ee3bbc1a',
            # 'RequestId': '673dc67-6dc7-11af-33ab-df11a89a22bc',
            # 'ActivityId': '9133bdb5-2138-f695-6975-f2ef50962769',
            'X-PowerBI-ResourceKey': '936cf53d-2714-4ddf-9471-f225d19461b1',
            'RequestId': '0b8e6b18-2c77-928b-681e-3c81dc09eb54',
            'ActivityId': 'fd30eec9-7039-85f2-d24c-515bc700f917',
        }

        # data = {"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"m","Entity":"medidas","Type":0},{"Name":"m2","Entity":"mfo_municipios","Type":0}],"Select":[{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL 1ª DOSE GERAL"},"Name":"medidas.total_1_dose"},{"Column":{"Expression":{"SourceRef":{"Source":"m2"}},"Property":"MUNICÍPIO"},"Name":"mfo_municipios.MUNICÍPIO"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL IMUNIZADOS"},"Name":"medidas.TOTAL IMUNIZADOS"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"% 1ª DOSE POR POPULACAO GERAL"},"Name":"medidas.% 1ª DOSE POR POPULACAO GERAL"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"% IMUNIZADOS POR POPULACAO GERAL"},"Name":"medidas.% IMUNIZADOS POR POPULACAO GERAL"}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0,1,2,3,4],"Subtotal":1}]},"DataReduction":{"DataVolume":3,"Primary":{"Window":{"Count":500}}},"Version":1},"ExecutionMetricsKind":1}}]},"CacheKey":"{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"m\",\"Entity\":\"medidas\",\"Type\":0},{\"Name\":\"m2\",\"Entity\":\"mfo_municipios\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL 1ª DOSE GERAL\"},\"Name\":\"medidas.total_1_dose\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m2\"}},\"Property\":\"MUNICÍPIO\"},\"Name\":\"mfo_municipios.MUNICÍPIO\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL IMUNIZADOS\"},\"Name\":\"medidas.TOTAL IMUNIZADOS\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"% 1ª DOSE POR POPULACAO GERAL\"},\"Name\":\"medidas.% 1ª DOSE POR POPULACAO GERAL\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"% IMUNIZADOS POR POPULACAO GERAL\"},\"Name\":\"medidas.% IMUNIZADOS POR POPULACAO GERAL\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}","QueryId":"","ApplicationContext":{"DatasetId":"7fb96090-5249-4e7e-b2bc-598c7e0d2c8e","Sources":[{"ReportId":"83b397f9-11b9-404e-8f40-889ffc3702af","VisualId":"eec7a79c32dbf13e4b7e"}]}}],"cancelQueries":[],"modelId":3864171}
        
        # Alteração na consulta, alterada no dia 04/11/2021
        data = {"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"m","Entity":"medidas","Type":0},{"Name":"m1","Entity":"mfo_municipios","Type":0}],"Select":[{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL 1ª DOSE GERAL"},"Name":"medidas.total_1_dose"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL IMUNIZADOS"},"Name":"medidas.TOTAL IMUNIZADOS"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"% 1ª DOSE POR POPULACAO GERAL"},"Name":"medidas.% 1ª DOSE POR POPULACAO GERAL"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"% IMUNIZADOS POR POPULACAO GERAL"},"Name":"medidas.% IMUNIZADOS POR POPULACAO GERAL"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL VACINAS APLIACADAS"},"Name":"medidas.TOTAL VACINAS APLIACADAS"},{"Measure":{"Expression":{"SourceRef":{"Source":"m"}},"Property":"TOTAL DOSE REFORÇO GERAL"},"Name":"medidas.TOTAL DOSE REFORÇO GERAL"},{"Column":{"Expression":{"SourceRef":{"Source":"m1"}},"Property":"MUNICÍPIO"},"Name":"mfo_municipios.MUNICÍPIO"}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0,1,2,3,4,5,6],"Subtotal":1}]},"DataReduction":{"DataVolume":3,"Primary":{"Window":{"Count":500}}},"Aggregates":[{"Select":2,"Aggregations":[{"Min":{}},{"Max":{}}]},{"Select":3,"Aggregations":[{"Min":{}},{"Max":{}}]}],"Version":1},"ExecutionMetricsKind":1}}]},"CacheKey":"{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"m\",\"Entity\":\"medidas\",\"Type\":0},{\"Name\":\"m1\",\"Entity\":\"mfo_municipios\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL 1ª DOSE GERAL\"},\"Name\":\"medidas.total_1_dose\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL IMUNIZADOS\"},\"Name\":\"medidas.TOTAL IMUNIZADOS\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"% 1ª DOSE POR POPULACAO GERAL\"},\"Name\":\"medidas.% 1ª DOSE POR POPULACAO GERAL\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"% IMUNIZADOS POR POPULACAO GERAL\"},\"Name\":\"medidas.% IMUNIZADOS POR POPULACAO GERAL\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL VACINAS APLIACADAS\"},\"Name\":\"medidas.TOTAL VACINAS APLIACADAS\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"TOTAL DOSE REFORÇO GERAL\"},\"Name\":\"medidas.TOTAL DOSE REFORÇO GERAL\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m1\"}},\"Property\":\"MUNICÍPIO\"},\"Name\":\"mfo_municipios.MUNICÍPIO\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Aggregates\":[{\"Select\":2,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]},{\"Select\":3,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1},\"ExecutionMetricsKind\":1}}]}","QueryId":"","ApplicationContext":{"DatasetId":"4f5da74a-d629-434a-adfe-1ba0d597969d","Sources":[{"ReportId":"59d0116c-b20a-4ffe-9376-c7109db83deb","VisualId":"350bde1b3069e389aaaa"}]}}],"cancelQueries":[],"modelId":3934596}
       
        print("Baixando dados dive 2... ", end='', flush=True)
        req_DB = requests.post(
            self.url, headers=self.headers, json=data).text
        print("Ok")

        # Carregando o arquivo JSON
        data_DB = json.loads(req_DB)
        if 'error' in data_DB:
            print("Erro!!!\n")
            if (data_DB['error']):
                print(data_DB['error'])
                return None
            else:
                raise Exception(data_DB['errorMessage']['title'] +
                                ": " + data_DB['errorMessage']['text'])

        # Extraindo a parte importante:
        self.dados = data_DB['results'][0]['result']['data']['dsr']['DS'][0]['PH'][1]['DM1']

        # Salvando apenas para fins de teste
        # with open('data_vacinacao.json', 'w') as f:
        #     json.dump(self.dados, f)

    def processa_dados(self):
        print("Processnado os dados... ", end='', flush=True)
        dados = self.dados
        dados_processado = list()
        
        for objeto in dados:
            if objeto['C']:
                dados_processado.append({
                    "municipio" : objeto['C'][0],
                    "d1" : objeto['C'][1],
                    "d2" : objeto['C'][2],
                    "percentual_d1" : float(objeto['C'][3]),
                    "percentual_d2" : float(objeto['C'][4]),
                   })
                
        # pprint.pprint(dados_processado)
        df = pd.DataFrame(dados_processado)
        
        # converte para tipo de dado correto
        df['d1'] = pd.to_numeric(df['d1'], errors='coerce', downcast='integer')
        df['d2'] = pd.to_numeric(df['d2'], errors='coerce', downcast='integer')
        df['percentual_d1'] = pd.to_numeric(df['percentual_d1'], errors='coerce', downcast='float')
        df['percentual_d2'] = pd.to_numeric(df['percentual_d2'], errors='coerce', downcast='float')
        
        # novas colunas
        df.insert(1, 'codigo_municipio', df['municipio'])
        df.insert(6, 'data_atualizacao', self.dataAtualizacao)
        
        # converte para para tipo data
        df['data_atualizacao'] = pd.to_datetime(self.dataAtualizacao.strftime("%Y-%m-%d")).date()
        
        # tenta substituir nome do municipio pelo codigo ibge
        try:
            df['codigo_municipio'] = df['codigo_municipio'].replace(self.municipios)
        except KeyError as k:
            raise Exception("Município não encontrado:" + k)
        
        # converte coluna para tipo integer
        df['codigo_municipio'] = pd.to_numeric(df['codigo_municipio'], errors='coerce', downcast='integer')
        
        # adiciona a coluna com a regional dos municipios
        df['regional'] = pd.Series([ self.tabelas.getRegionalMunicipioBrasil(line) for line in df['codigo_municipio'] ])
        
        print("Ok")
        return df
    
    def connect(self, params_dic):
        try:
            conn = psycopg2.connect(**params_dic)
            conn.autocommit = True
            self.conn = conn
            # print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn
    
    def salva_bd(self, df, table='vacinacao_dive2'):
        
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
        print(" Ok")

# if __name__ == "__main__":
#     try:
#         vacinados = download_vacinados2()
#         df = vacinados.processa_dados()
#         vacinados.salva_bd(df)
#     except Exception as message:
#         print(f"Erro: {message}")
