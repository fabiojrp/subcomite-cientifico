import csv
from Utils import Utils
from dao.DadosDao import DadosDao
from db.create import Create 
from datetime import datetime

create = Create()
create.create_leitos()

dadosDao = DadosDao()

today = datetime.now()
att = today.strftime('%Y-%m-%d %H:%M:%S')

print("Inserindo os dados de leitos...")
with open('Leitos COVID - Leitos Geral+Covid.csv', 'r') as arquivo_leitos:
    hospitais = csv.DictReader(arquivo_leitos, delimiter=",")

    for hospital in hospitais:
        # print(hospital)
        if hospital['macrorregiao'] == '':
            break    

        hospital['taxa_ocupacao'] = hospital['taxa_ocupacao'].replace(',','.',1)
        hospital['taxa_ocupacao'] = hospital['taxa_ocupacao'].replace('%','',1)

        params = (
            hospital['macrorregiao'],
            hospital['hospital'],
            hospital['municipio'],
            Utils.convert_to_int(hospital['codigo_ibge_municipio']),
            hospital['regional_saude'],
            Utils.convert_to_int(hospital['index_regional']),
            Utils.convert_to_int(hospital['leitos_ativos']),
            Utils.convert_to_int(hospital['leitos_ocupados']),
            Utils.convert_to_int(hospital['leitos_disponiveis']),
            Utils.convert_to_float(hospital['taxa_ocupacao']),
            Utils.convert_to_int(hospital['pacientes_covid']),
            att
        )

        dadosDao.leitos_Gerais_Covid(params)

with open('Leitos COVID - Apenas leitos COVID.csv', 'r') as arquivo_leitos:
    hospitais = csv.DictReader(arquivo_leitos, delimiter=",")

    for hospital in hospitais:
        # print(hospital)
        if hospital['Hospital'] == '':
            break    

        hospital['Taxa de Ocupação'] = hospital['Taxa de Ocupação'].replace(',','.',1)
        hospital['Taxa de Ocupação'] = hospital['Taxa de Ocupação'].replace('%','',1)

        params = (
            hospital['Macrorregião'],
            hospital['Hospital'],
            hospital['municipio'],
            Utils.convert_to_int(hospital['codigo_ibge_municipio']),
            hospital['regional_saude'],
            Utils.convert_to_int(hospital['index_regional']),
            Utils.convert_to_int(hospital['Leitos Ativos']),
            Utils.convert_to_int(hospital['Leitos Ocupados']),
            Utils.convert_to_int(hospital['Leitos Disponíveis']),
            Utils.convert_to_float(hospital['Taxa de Ocupação']),
            Utils.convert_to_int(hospital['Pacientes COVID']),
            att
        )

        dadosDao.leitos_Covid(params)

print("Ok")