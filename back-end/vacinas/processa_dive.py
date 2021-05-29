import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

file_path = os.getcwd() + \
    '/back-end/vacinas/COM_REGISTRO DE DOSES APLICADAS COVID-19 26.05.2021.xlsx'

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

with open(os.getcwd() + '/back-end/vacinas/municipios.txt') as f:
    dadosMunicipio = f.read().upper()
# reconstructing the data as a dictionary
municipios = json.loads(dadosMunicipio)

if not os.path.isfile(file_path):
    raise 'Arquivo não existe' + file_path
df = pd.read_excel(file_path,
                   sheet_name="COMUNICAÇÃO",
                   usecols=usarColunas
                   )
# Renomeia as colunas:
df.columns = nomeColunas

# Busca na listas os munícipios e substitui pelo código do IBGE
df['MUNICÍPIO'] = df['MUNICÍPIO'].replace(municipios)

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
fileSplit = file_path.split(".")
dataTexto = fileSplit[-4].split(" ")[-1] + "/" + \
    fileSplit[-3] + "/" + fileSplit[-2]
data = datetime.strptime(dataTexto, '%d/%m/%Y').date()
df.insert(0, "Data", data)

#apaga a linha do total do Estado marcada como: SEM DEFICIENTES ILPI E COMORBIDADES
df = df.drop(df.index[-1])

# for i, j in df.iterrows():
#     print(i, ";", j['MUNICÍPIO'])

print(df)
