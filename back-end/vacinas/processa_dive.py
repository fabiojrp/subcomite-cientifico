import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from pandas import ExcelWriter
import psycopg2
from io import StringIO
from sqlalchemy import create_engine
from urllib.parse import quote
from os import listdir
from os.path import isfile


class processa_dive():
    def __init__(self):
        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "!admpasswd@covid"
        }

        self.db = self.connect(self.param_dic)

        with open(os.getcwd() + '/back-end/vacinas/municipios.txt') as f:
            self.dadosMunicipio = f.read().upper()
        # Reconstruindo a lista dos munícipios.
        self.municipios = json.loads(self.dadosMunicipio)

    def buscaArquivos(self):
        dir_path = os.getcwd() + \
            '/back-end/vacinas/balancos/'
        for f in listdir(dir_path):
            if isfile(dir_path + f) and (f.split(".")[-1] == 'xlsx'):
                print("Arquivo: " + f)
                df = self.extraiDados(dir_path + f, f)
                processa_dive.salvaBD(df, self.param_dic)

    # df = processa_dive.extraiDados(
    #     'COM_REGISTRO DE DOSES APLICADAS COVID-19 26.05.2021.xlsx')

    def extraiDados(self, file_path, file):
        usarColunas = "A,B,D,F,H,J,K,L,N,P,R,T,V,X,Z,AB,AD,AF, \
                    AH,AJ,AL,AN,AP,AR,AT,AV,AX,AZ,BA,BB,BD,BF,BH,\
                    BJ,BL"

        nomeColunas = ['MUNICÍPIO',
                       'TRABALHADORES DA SAUDE-D1',
                       'TRABALHADORES DA SAUDE-D2',
                       'PESSOAS IDOSAS INSTITUCIONALIZADAS-D1',
                       'PESSOAS IDOSAS INSTITUCIONALIZADAS-D2',
                       'PESSOAS COM DEFICIÊNCIA INSTITUCIONALIZADA-D1',
                       'PESSOAS COM DEFICIÊNCIA INSTITUCIONALIZADA-D2',
                       'POPULAÇÃO INDÍGENA-D1',
                       'POPULAÇÃO INDÍGENA-D2',
                       'IDOSOS COM 90 ANOS E MAIS-D1',
                       'IDOSOS COM 90 ANOS E MAIS-D2',
                       'IDOSOS COM 85 a 89 ANOS-D1',
                       'IDOSOS COM 85 a 89 ANOS-D2',
                       'IDOSOS COM 80 a 84 ANOS-D1',
                       'IDOSOS COM 80 a 84 ANOS-D2',
                       'IDOSOS COM 75 a 79 ANOS-D1',
                       'IDOSOS COM 75 a 79 ANOS-D2',
                       'IDOSOS COM 70 a 74 ANOS-D1',
                       'IDOSOS COM 70 a 74 ANOS-D2',
                       'IDOSOS COM 65 a 69 ANOS-D1',
                       'IDOSOS COM 65 a 69 ANOS-D2',
                       'IDOSOS COM 60 a 64 ANOS-D1',
                       'IDOSOS COM 60 a 64 ANOS-D2',
                       'QUILOMBOLA-D1',
                       'QUILOMBOLA-D2',
                       'FORÇAS DE SEGURANÇA E SALVAMENTO E FORÇAS ARMADAS-D1',
                       'FORÇAS DE SEGURANÇA E SALVAMENTO E FORÇAS ARMADAS-D2',
                       'COMORBIDADE DE 18 A 59 ANOS-D1',
                       'COMORBIDADE DE 18 A 59 ANOS-D2',
                       'PESSOAS COM DEFICIÊNCIA PERMANENTE GRAVE DE 18 A 59 ANOS-D1',
                       'PESSOAS COM DEFICIÊNCIA PERMANENTE GRAVE DE 18 A 59 ANOS-D2',
                       'GESTANTES E PUÉRPERAS-D1',
                       'GESTANTES E PUÉRPERAS-D2',
                       'TOTAL-D1',
                       'TOTAL-D2']

        if not os.path.isfile(file_path):
            raise 'Arquivo não existe' + file_path
        df = pd.read_excel(file_path,
                           sheet_name="COMUNICAÇÃO",
                           usecols=usarColunas
                           )
        
        limitTable = list(df).index('TOTAL') + 4    
        # Renomeia as colunas:
        df.columns = nomeColunas

        # Busca na listas os munícipios e substitui pelo código do IBGE
        df['MUNICÍPIO'] = df['MUNICÍPIO'].replace(self.municipios)

        # Converte valores para Int
        df['MUNICÍPIO'] = pd.to_numeric(
            df['MUNICÍPIO'], errors='coerce', downcast='integer')

        # apaga o que não for valor
        df = df[df['MUNICÍPIO'].notna()]

        #  converte todos os valores para números
        df = df.apply(pd.to_numeric)

        # atribui a coluna dos munícipios como Int
        df['MUNICÍPIO'] = df['MUNICÍPIO'].astype(int)

        # Insere a data dos dados:
        fileSplit = file.split(".")
        dataTexto = fileSplit[-4].split(" ")[-1] + "/" + \
            fileSplit[-3] + "/" + fileSplit[-2]
        data = datetime.strptime(dataTexto, '%d/%m/%Y').date()
        df.insert(0, "Data", data)

        # apaga a linha do total do Estado marcada como: SEM DEFICIENTES ILPI E COMORBIDADES
        df = df.drop(df.index[-1])

        with ExcelWriter('dados.xlsx') as writer:
            df.to_excel(writer, sheet_name='df')
            df.filter(regex='D1', axis=1).to_excel(writer, sheet_name='D1')
            df.filter(regex='D2', axis=1).to_excel(writer, sheet_name='D2')

        return df
        # print(df)

    def connect(self, params_dic):
        try:
            conn = psycopg2.connect(**params_dic)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn

    def salvaBD(self, df, param_dic, table='vacinacao'):
        # Cria a tabela se não existe
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
            # if_exists='append'
            if_exists='replace'
        )

        print("Salvando...", end='', flush=True)
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

    processa_dive = processa_dive()
    processa_dive.buscaArquivos()
