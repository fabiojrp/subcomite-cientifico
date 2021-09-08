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
tabelas = tabelas.Tabelas()
estatistica = processa.estatistica()
dadosDao = DadosDao()

create.create_table_brasil()

index = 0

casos_municipios = {}
casos_acumulados_municipios = {}

# Para montagem da média móvel
data_inicio = datetime.datetime(2020, 2, 25, 0, 0)
data_fim = datetime.datetime.today()
datas_casos = [data_inicio + datetime.timedelta(n)
               for n in range(int((data_fim - data_inicio).days)+1)]

start_time = time.time()
print("Inserido os dados na tabela...")
# with open('HIST_PAINEL_COVIDBR_27jan2021.csv', 'r') as arquivo:
with open('HIST_PAINEL_COVIDBR.csv', 'r') as arquivo:
    dados = csv.DictReader(arquivo, delimiter=";")
    #LinhasTotaisCsv = len(dados)
    for value in dados:
        index = index + 1
        if index % 100000 == 0:
            print(index, flush=True)
        elif index % 10000 == 0:
            print(index, end='', flush=True)
        elif index % 1000 == 0:
            print('.', end='', flush=True)

        if (value['estado'] != 'SC'):
            continue

        try:
            data = Utils.date_format(value['data'])
        except ValueError as ex:
            data = datetime.datetime(2020, 1, 1, 0, 0)

        codigo_ibge_municipio = Utils.convert_to_int(value['codmun'])

        val = (
            value['regiao'],
            value['estado'],
            value['municipio'],
            Utils.convert_to_int(value['coduf']),
            codigo_ibge_municipio,
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

        # Controe um dicionário no formato:
        # Municipio : {Data : Casos}
        if casos_municipios.get(codigo_ibge_municipio) == None:
            casos_municipios[codigo_ibge_municipio] = {
                'regional': tabelas.getRegionalMunicipioBrasil(codigo_ibge_municipio),
                'populacao': Utils.convert_to_int(value['populacaoTCU2019']),
                'datas': {}}

            for key in datas_casos:
                casos_municipios[codigo_ibge_municipio]['datas'][key] = dict(
                    casos=0,
                    obitos=0,
                    casos_acumulados=0,
                    obitos_acumulados=0,
                    casos_mediaMovel=0,
                    obitos_mediaMovel=0,
                    variacao_mediaMovel_casos=0,
                    casos_acumulados_100mil=0,
                    obitos_acumulados_100mil=0,
                    casos_variacao_14dias=0,
                    obitos_variacao_14dias=0,
                    incidencia_casos_diarios_100mil=0,
                    incidencia_obitos_diarios_100mil=0,
                    letalidade_100_confirmados=0,
                    incidencia_100mil=0,
                    dt_letalidade=0,
                    casos_ativos=0
                )

        casos_municipios[codigo_ibge_municipio]['datas'][data]['casos'] = Utils.convert_to_int(
            value['casosNovos'])
        casos_municipios[codigo_ibge_municipio]['datas'][data]['obitos'] = Utils.convert_to_int(
            value['obitosNovos'])
        #casos_municipios[codigo_ibge_municipio]['datas'][data]['casos_acumulados'] =  Utils.convert_to_int(value['casosAcumulado'])
        #casos_municipios[codigo_ibge_municipio]['datas'][data]['obitos_acumulados'] =  Utils.convert_to_int(value['obitosAcumulado'])


print('Fim', flush=True)

estatistica.processamento(casos_municipios)
print("\n\nInserido os casos filtrados na tabela...")

dadosDao.casos_municipios(casos_municipios)

print("\n\nConcluido\n")
print("\n--- %s seconds ---\n" % (time.time() - start_time))
