import csv
import os
import datetime
import time
from db.create import Create
from dao.DadosDao import DadosDao
from Utils import Utils
from dados import tabelas
from processa import processa

create = Create()
tabelas = tabelas.Tabelas();
#estatistica = processa.estatistica();
dadosDao = DadosDao()

create.create_table_brasil()

index = 0

casos_municipios = {}
casos_acumulados_municipios = {}

# Para montagem da média móvel
data_inicio = datetime.datetime(2020,2,25, 0, 0)
data_fim = datetime.datetime.today()
datas_casos = [ data_inicio + datetime.timedelta(n) for n in range(int ((data_fim - data_inicio).days)+1)]

start_time = time.time();
print("Inserido os dados na tabela...")
with open('HIST_PAINEL_COVIDBR_27jan2021.csv', 'r') as arquivo:
#with open('dados_1000.csv', 'r') as arquivo:
    dados = csv.DictReader(arquivo, delimiter=";")
    #LinhasTotaisCsv = len(dados)
    for value in dados:
        try:
            data = Utils.date_format(value['data'])
        except ValueError as ex:
            data = datetime.datetime(2020, 1, 1, 0, 0)

        if (value['estado'] != 'SC'):
            continue;

        val = (
            value['regiao'],
            value['estado'],
            value['municipio'],
            Utils.convert_to_int(value['coduf']),
            Utils.convert_to_int(value['codmun']),
            Utils.convert_to_int(value['codRegiaoSaude']),
            value['nomeRegiaoSaude'],
            data,
            Utils.convert_to_int(value['semanaEpi']),
            Utils.convert_to_int(value['populacaoTCU2019']),
            Utils.convert_to_int(value['casosAcumulado']),
            Utils.convert_to_int(value['casosNovos']),
            Utils.convert_to_int(value['obitosAcumulado']),
            Utils.convert_to_int(value['obitosNovos']),
            Utils.convert_to_int(value['Recuperadosnovos']),
            Utils.convert_to_int(value['emAcompanhamentoNovos']),
            Utils.convert_to_int(value['interior/metropolitana']),
        )

        dadosDao.insertBrasil(val)
        
        index = index + 1
        if index % 100000 == 0:
            print(index, flush=True)
        elif index % 10000 == 0:
            print(index, end='', flush=True)
        elif index % 1000 == 0:
            print('.', end='', flush=True)
print('Fim', flush=True)        
#estatistica.(casos_municipios)
print("\n\nInserido os casos filtrados na tabela...") 

dadosDao.casos_municipios(casos_municipios)

print("\n\nConcluido\n")
print("\n--- %s seconds ---\n" % (time.time() - start_time))
