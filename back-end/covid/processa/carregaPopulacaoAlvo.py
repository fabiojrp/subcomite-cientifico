import pandas as pd
import numpy as np
import json
import os
import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote    
class carregaPopulacaoAlvo():
    
    def __init__(self):
        self.grupos_etarios = {
            "Mais de 100 anos": 0,
            "95 a 99 anos":1,
            "90 a 94 anos":2,
            "85 a 89 anos":3,
            "80 a 84 anos":4,
            "75 a 79 anos":5,
            "70 a 74 anos":6,
            "65 a 69 anos":7,
            "60 a 64 anos":8,
            "55 a 59 anos":9,
            "50 a 54 anos":10,
            "45 a 49 anos":11,
            "40 a 44 anos":12,
            "35 a 39 anos":13,
            "30 a 34 anos":14,
            "25 a 29 anos":15,
            "20 a 24 anos":16,
            "15 a 19 anos":17,
            "10 a 14 anos":18,
            "5 a 9 anos":19,
            "0 a 4 anos": 20
        }
        
        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "!admpasswd@covid"
        }

        self.db = self.connect(self.param_dic)

        # with open(os.getcwd() + '/back-end/covid/processa/vacinas/municipios.txt') as f:
        with open(os.getcwd() + '/vacinas/municipios.txt') as f:
            self.dadosMunicipio = f.read().upper()
        # Reconstruindo a lista dos munícipios.
        self.municipios = json.loads(self.dadosMunicipio)
        
    def connect(self, params_dic):
        try:
            conn = psycopg2.connect(**params_dic)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn

    def salvaBD(self, df, param_dic, table='populacao_alvo'):

        connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            param_dic['user'],
            quote(param_dic['password']),
            param_dic['host'],
            param_dic['database']
        )
        engine = create_engine(connect)
        df.to_sql(
            table,
            con=engine,
            index=False,
            if_exists='append'
            # if_exists='replace'
        )
        
    def busca_dados(self):
        # 422000, 421265, 0
        base_url = "https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?ano=2010&wmaxbarra=140&cormulher=d8fe35&corhomem=41c300&codigo={}"

        for municipio, municipio_ in self.municipios.items():
            if municipio_ == 0:
                df_mun = pd.read_html(io=(base_url.format(42)), thousands='.', skiprows=[22])
            elif municipio_ == 422000 or municipio_ == 421265:
                continue
            else:
                df_mun = pd.read_html(io=(base_url.format(municipio_)), thousands='.', skiprows=[22])
            
            # retira da lista
            df_mun = df_mun[0]
            
            # remove colunas de proporção em relação ao total do municipio
            df_mun.pop(2)
            df_mun.pop(3)

            # remove ultimo elemento
            df_mun = df_mun.drop(df_mun.index[-1:])

            # renomeia coluna
            df_mun.rename({0: "grupo_etario", 1: "pop_masculino", 4: "pop_feminino"}, axis=1, inplace=True)

            # tenta converter para inteiro
            df_mun['pop_feminino'] = pd.to_numeric(df_mun['pop_feminino'], errors='raise', downcast='integer')
            df_mun['pop_masculino'] = pd.to_numeric(df_mun['pop_masculino'], errors='raise', downcast='integer')
            
            # preenche com 0 valores nulos
            df_mun.fillna(0, inplace=True)
            
            # tranforma colunas para tipo int
            df_mun['pop_feminino'] = df_mun['pop_feminino'].astype(int)
            df_mun['pop_masculino'] = df_mun['pop_masculino'].astype(int)

            # adiciona colunas do municipio, soma da população etária e id do grupo prioritario
            df_mun.insert(0, "municipio", municipio)
            df_mun.insert(1, "codigo_municipio", municipio_)
            df_mun.insert(5, "populacao_etaria", (df_mun["pop_feminino"] + df_mun["pop_masculino"]))
            df_mun.insert(3, "id_grupo_etario", df_mun['grupo_etario'])
            
            # substitui pelo id
            df_mun['id_grupo_etario'] = df_mun['id_grupo_etario'].replace(self.grupos_etarios)
            
            # df_mun.info()
            # print(df_mun)
            
            self.salvaBD(df_mun, self.param_dic)


if __name__ == "__main__":
    carregaPopulacaoAlvo = carregaPopulacaoAlvo()
    carregaPopulacaoAlvo.busca_dados()