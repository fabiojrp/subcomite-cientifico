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
estatistica = processa.estatistica();
dadosDao = DadosDao()

create.create_table()

index = 0

casos_municipios = {}
casos_acumulados_municipios = {}

# Para montagem da média móvel
data_inicio = datetime.datetime(2020,2,25, 0, 0)
data_fim = datetime.datetime.today()
datas_casos = [ data_inicio + datetime.timedelta(n) for n in range(int ((data_fim - data_inicio).days)+1)]

start_time = time.time();
print("Inserido os dados na tabela...")
with open('boavista_covid_dados_abertos.csv', 'r') as arquivo:
#with open('dados_1000.csv', 'r') as arquivo:
    dados = csv.DictReader(arquivo, delimiter=";")
    #LinhasTotaisCsv = len(dados)
    for value in dados:
            
        data_publicacao = Utils.datetime_format(value['data_publicacao'])
        if (data_publicacao == -1):
            print(value)
            continue
        data_inicio_sintomas = Utils.date_format(value['data_inicio_sintomas'])
        if (data_inicio_sintomas == -1):
            print(value)
            continue
        data_resultado = Utils.date_format(value['data_resultado']);
        if (data_resultado == -1):
            print(value)
            continue
        data_obito = None
        data_entrada_uti = None
        data_internacao = None
        data_evolucao_caso = None
        data_saida_uti = None
        data_coleta = None
        
        #if data_resultado > data_inicio:
        #    data_referencia = data_resultado
        #else:
        data_referencia = data_inicio_sintomas

        if value['data_coleta'] != 'IGNORADO':
            data_coleta = Utils.date_format(value['data_coleta'])

        if value['data_obito'] != 'NULL':
            data_obito = Utils.date_format(value['data_obito'])

        if value['data_internacao'] != 'NULL':
            data_internacao = Utils.date_format(value['data_internacao'])

        if value['data_entrada_uti'] != 'NULL':
            data_entrada_uti = Utils.date_format(value['data_entrada_uti'])

        if value['data_evolucao_caso'] != 'NULL':
            data_evolucao_caso = Utils.date_format(value['data_evolucao_caso'])

        if value['data_saida_uti'] != 'NULL':
            data_saida_uti = Utils.date_format(value['data_saida_uti'])

        if value['idade'] == 'NULL':
            idade = -1
        else:
            idade = value['idade']

        try:
            codigo_ibge_municipio = int(value['codigo_ibge_municipio']);
        except ValueError as ex:
            codigo_ibge_municipio = 0;

        try:
            codigo_ibge_municipio_notificacao = int(value['codigo_ibge_municipio_notificacao']);
        except ValueError as ex:
            codigo_ibge_municipio_notificacao = 0;


        val = (
            data_publicacao,
            value['recuperados'],
            data_inicio_sintomas,
            data_coleta,
            ",".join(map(str.strip, value['sintomas'].split(","))),
            ",".join(map(str.strip, value['comorbidades'].split(","))),
            ",".join(map(str.strip, value['gestante'].split(","))),
            value['internacao'],
            value['internacao_uti'],
            value['sexo'],
            value['municipio'],
            value['obito'],
            data_obito,
            idade,
            value['regional'],
            value['raca'],
            data_resultado ,
            codigo_ibge_municipio,
            value['latitude'],
            value['longitude'],
            value['estado'],
            value['criterio_confirmacao'],
            value['tipo_teste'],
            value['municipio_notificacao'],
            codigo_ibge_municipio_notificacao,
            value['latitude_notificacao'],
            value['longitude_notificacao'],
            value['classificacao'],
            value['origem_esus'],
            value['origem_sivep'],
            value['origem_lacen'],
            value['origem_laboratorio_privado'],
            value['nom_laboratorio'],
            value['fez_teste_rapido'],
            value['fez_pcr'],
            data_internacao,
            data_entrada_uti,
            value['regional_saude'],
            data_evolucao_caso,
            data_saida_uti,
            value['bairro'],

        )
        dadosDao.insert(val)
        
        #Número de casos e obitos por município por dia
        #Controe um dicionário no formato:
        # Municipio : {Data : Casos}
        if casos_municipios.get(codigo_ibge_municipio)==None: 
            #casos_municipios[codigo_ibge_municipio] = {'regional': 0, 'datas':{}}
            casos_municipios[codigo_ibge_municipio] = {
                'regional': tabelas.getRegionalMunicipio(codigo_ibge_municipio),
                'populacao': tabelas.getPopulacaoMunicipio(codigo_ibge_municipio),
                'datas':{}}

            for key in datas_casos: 
                casos_municipios[codigo_ibge_municipio]['datas'][key] = dict(
                    casos =  0, 
                    obitos= 0, 
                    casos_acumulados=0, 
                    obitos_acumulados = 0,
                    casos_mediaMovel = 0,
                    obitos_mediaMovel = 0,
                    casos_acumulados_100mil = 0, 
                    obitos_acumulados_100mil = 0,
                    casos_variacao_14dias = 0,
                    obitos_variacao_14dias = 0,
                    incidencia_casos_diarios_100mil = 0,
                    incidencia_obitos_diarios_100mil = 0,
                    letalidade_100_confirmados = 0,
                    incidencia_100mil = 0,
                    casos_ativos = 0,
                )


        casos_municipios[codigo_ibge_municipio]['datas'][data_referencia]['casos']+=1
        
        for datas in datas_casos:  
            if value['recuperados'] == 'SIM' and value['obito'] == 'NAO':
                if data_evolucao_caso != None:
                    if Utils.date_check(data_inicio_sintomas, data_evolucao_caso, datas) == True:
                        casos_municipios[codigo_ibge_municipio]['datas'][datas]['casos_ativos']+=1
                    else:
                        continue
                else:
                    string_data_inicio = datetime.datetime.strptime(value['data_inicio_sintomas'], '%Y-%m-%d')
                    data_recuperacao = (string_data_inicio + datetime.timedelta(days=14))

                    if Utils.date_check(string_data_inicio, data_recuperacao, datas) == True:
                        casos_municipios[codigo_ibge_municipio]['datas'][datas]['casos_ativos']+=1
                    else:
                        continue

            elif value['obito'] == 'NAO' and value['recuperados'] == 'NAO':
                if Utils.date_check_atived(data_inicio_sintomas, datas) == True:
                    casos_municipios[codigo_ibge_municipio]['datas'][datas]['casos_ativos']+=1

            elif value['obito'] == 'SIM':
                if Utils.date_check(data_inicio_sintomas,data_obito,datas) == True:
                    casos_municipios[codigo_ibge_municipio]['datas'][datas]['casos_ativos']+=1
                else:
                    continue
        
        if data_obito != None:
            casos_municipios[codigo_ibge_municipio]['datas'][data_obito]['obitos']+=1
         
            #Número de óbitos acumulados por município por dia
            #for dataPesquisa in datas_casos:
            #    if dataPesquisa >= data_obito:
            #        casos_municipios[codigo_ibge_municipio]['datas'][dataPesquisa]['obitos_acumulados']+=1
 

        #Número de casos acumulados por município por dia
        #for datasPesquisa in datas_casos:
        #    if datasPesquisa >= data_referencia:
        #        casos_municipios[codigo_ibge_municipio]['datas'][datasPesquisa]['casos_acumulados']+=1

        index = index + 1
        if index % 100000 == 0:
            print(index, flush=True)
        elif index % 10000 == 0:
            print(index, end='', flush=True)
        elif index % 1000 == 0:
            print('.', end='', flush=True)
print('Fim', flush=True)        
estatistica.processamento(casos_municipios)
print("\n\nInserido os casos filtrados na tabela...") 

dadosDao.casos_municipios(casos_municipios)

print("\n\nConcluido\n")
print("\n--- %s seconds ---\n" % (time.time() - start_time))
