import urllib.request
import json
import requests
from xml.dom import minidom
import urllib
from covid.processa.processaLeitos import processaLeitos
from covid.processa.dao.DadosDao import DadosDao
from covid.processa.db.create import Create
from datetime import datetime


class download_leitos:
    def __init__(self, simulacao=0):
        create = Create()
        create.create_leitos()
        dadosDao = DadosDao()
        dataAtualizacao = datetime.now()

        self.url = ' https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true'

        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'wabi-brazil-south-api.analysis.windows.net',
            'Origin': 'https://app.powerbi.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Referer': 'https://app.powerbi.com/',
            'Content-Length': '4288',
            'Connection': 'keep-alive',
            'X-PowerBI-ResourceKey': '1807b851-3dab-4963-bb2f-94f60ffc8ccc',
            'RequestId': '9dbdda0c-9079-3ae9-2203-df87d14b398d',
            'ActivityId': 'a07afce7-9752-4356-a44f-9bb724e08c55',
        }

        leitos = {}
        for tipo in range(1, 3):
            leitos[tipo] = {}
            if tipo == 1:
                print("Validando os leitos COVID apenas Adulto... ")
                # Consulta de casos Covid Tipo de Leito: Adulto, Apenas Leitos COVID
                data = {"version": "1.0.0", "queries": [{"Query": {"Commands": [{"SemanticQueryDataShapeCommand": {"Query": {"Version": 2, "From": [{"Name": "f", "Entity": "fat_leitos_hospitalares", "Type": 0}, {"Name": "#", "Entity": "#Medidas 1 - Quantitativos Gerais", "Type": 0}, {"Name": "d", "Entity": "dim_macrorregioes", "Type": 0}], "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "hospital"}, "Name": "fat_leitos_hospitalares.hospital"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ativos"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ativos"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ocupados"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ocupados"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Disponíveis"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Disponíveis"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Taxa de Ocupação"}, "Name": "#Medidas 1 - Quantitativos Gerais.Taxa de Ocupação"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Pacientes COVID Internados"},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          "Name": "#Medidas 1 - Quantitativos Gerais.{GAL} Internados COVID (Conf&Susp)"}, {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}, "Name": "dim_macrorregioes.macro_desc_ac"}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "Leito COVID 2"}}], "Values": [[{"Literal": {"Value": "'COVID'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "classificacao"}}], "Values": [[{"Literal": {"Value": "'uti'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_tipo"}}], "Values": [[{"Literal": {"Value": "'ADULTO'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_sus"}}], "Values": [[{"Literal": {"Value": "true"}}]]}}}], "OrderBy": [{"Direction": 1, "Expression": {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}}}]}, "Binding": {"Primary": {"Groupings": [{"Projections": [0, 1, 2, 3, 4, 5, 6], "Subtotal":1}]}, "DataReduction":{"DataVolume": 3, "Primary": {"Window": {"Count": 500}}}, "Version": 1}}}]}, "QueryId": "", "ApplicationContext": {"DatasetId": "0c400f04-4bb2-4414-867e-790bdd9dcd5f", "Sources": [{"ReportId": "e585da1e-bcb4-46d8-ad92-6dc8640f59ed"}]}}], "cancelQueries": [], "modelId": 2604433}
            if tipo == 2:
                print("Validando os leitos GERAL apenas Adulto... ")
                # Consulta de casos Covid Tipo de Leito: Adulto, Leitos Geral
                data = {"version": "1.0.0", "queries": [{"Query": {"Commands": [{"SemanticQueryDataShapeCommand": {"Query": {"Version": 2, "From": [{"Name": "f", "Entity": "fat_leitos_hospitalares", "Type": 0}, {"Name": "#", "Entity": "#Medidas 1 - Quantitativos Gerais", "Type": 0}, {"Name": "d", "Entity": "dim_macrorregioes", "Type": 0}], "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "hospital"}, "Name": "fat_leitos_hospitalares.hospital"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ativos"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ativos"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ocupados"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ocupados"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Disponíveis"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Disponíveis"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Taxa de Ocupação"}, "Name": "#Medidas 1 - Quantitativos Gerais.Taxa de Ocupação"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Pacientes COVID Internados"},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          "Name": "#Medidas 1 - Quantitativos Gerais.{GAL} Internados COVID (Conf&Susp)"}, {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}, "Name": "dim_macrorregioes.macro_desc_ac"}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "Leito COVID 2"}}], "Values": [[{"Literal": {"Value": "'COVID'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "classificacao"}}], "Values": [[{"Literal": {"Value": "'uti'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_tipo"}}], "Values": [[{"Literal": {"Value": "'ADULTO'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_sus"}}], "Values": [[{"Literal": {"Value": "true"}}]]}}}], "OrderBy": [{"Direction": 1, "Expression": {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}}}]}, "Binding": {"Primary": {"Groupings": [{"Projections": [0, 1, 2, 3, 4, 5, 6], "Subtotal":1}]}, "DataReduction":{"DataVolume": 3, "Primary": {"Window": {"Count": 500}}}, "Version": 1}}}]}, "QueryId": "", "ApplicationContext": {"DatasetId": "0c400f04-4bb2-4414-867e-790bdd9dcd5f", "Sources": [{"ReportId": "e585da1e-bcb4-46d8-ad92-6dc8640f59ed"}]}}], "cancelQueries": [], "modelId": 2604433}

            req_DB = requests.post(
                self.url, headers=self.headers, json=data).text

            data_DB = json.loads(req_DB)

            hospitais = data_DB['results'][0]['result']['data']['dsr']['DS'][0]['ValueDicts']['D0']
            valores = data_DB['results'][0]['result']['data']['dsr']['DS'][0]['PH'][1]['DM1']
            totais = data_DB['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['C']

            for i in range(len(hospitais)):
                infoHospital = processaLeitos.buscaInfoHospital(hospitais[i])
                if infoHospital == -1:
                    break

                infoHospital['hospital'] = hospitais[i]
                valorHospital = valores[i]['C']
                # print(i, ";", hospitais[i], ";", valorHospital)
                
                if not('R' in valores[i]):
                    # print(i, ";", hospitais[i], ";", valorHospital)
                    infoHospital['leitos_ativos'] = valorHospital[2]
                    infoHospital['leitos_ocupados'] = valorHospital[3]
                    infoHospital['leitos_disponiveis'] = valorHospital[2] - \
                        valorHospital[3]
                    if len(valorHospital) == 6:
                        infoHospital['pacientes_covid'] = valorHospital[5]
                    elif len(valorHospital) == 7:
                        infoHospital['pacientes_covid'] = valorHospital[6]
                    elif valores[i]['Ø'] == 80:
                        infoHospital['pacientes_covid'] = 0
                    else:
                        raise Exception("!-- Erro processando: ", i, ";",
                                        hospitais[i], ";", valorHospital)
                else:
                    if valores[i]['R'] == 2:
                        if 'Ø' in valores[i]:
                            if valores[i]['Ø'] == 104:
                                infoHospital['leitos_ativos'] = valorHospital[1]
                                infoHospital['leitos_ocupados'] = 0
                                infoHospital['leitos_disponiveis'] = valorHospital[2]
                                infoHospital['pacientes_covid'] = 0
                            elif valores[i]['Ø'] == 80:
                                infoHospital['leitos_ativos'] = valorHospital[1]
                                infoHospital['leitos_ocupados'] = valorHospital[2]
                                infoHospital['leitos_disponiveis'] = valorHospital[1] - valorHospital[2]
                                infoHospital['pacientes_covid'] = 0  
                            elif valores[i]['Ø'] == 64:
                                infoHospital['leitos_ativos'] = valorHospital[1]
                                infoHospital['leitos_ocupados'] = valorHospital[2]
                                infoHospital['leitos_disponiveis'] = valorHospital[3]
                                infoHospital['pacientes_covid'] = 0    
                            else:
                                infoHospital['leitos_ativos'] = valorHospital[1]
                                infoHospital['leitos_ocupados'] = valorHospital[2]
                                infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                                    valorHospital[2]
                                infoHospital['pacientes_covid'] = valorHospital[4]
                            # print(i, ";", hospitais[i], ";",
                            #  valorHospital, ";", valores[i]['R'])
                        else:
                            infoHospital['leitos_ativos'] = valorHospital[1]
                            infoHospital['leitos_ocupados'] = valorHospital[2]
                            infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                                valorHospital[2]
                            infoHospital['pacientes_covid'] = valorHospital[5]
                        # print(i, ";", hospitais[i], ";", valorHospital,
                        #   ";", valores[i]['R'], ";", valores[i]['Ø'])
                    elif valores[i]['R'] == 6:
                        if 'Ø' in valores[i]:
                            infoHospital['leitos_ativos'] = valorHospital[1]
                            infoHospital['leitos_ocupados'] = valorHospital[1]
                            infoHospital['leitos_disponiveis'] = 0
                            infoHospital['pacientes_covid'] = valorHospital[3]
                        else:
                            infoHospital['leitos_ativos'] = valorHospital[1] + \
                                valorHospital[2]
                            infoHospital['leitos_ocupados'] = valorHospital[1]
                            infoHospital['leitos_disponiveis'] = valorHospital[2]
                            infoHospital['pacientes_covid'] = valorHospital[4]

                    elif valores[i]['R'] == 10:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[1]
                        if 'Ø' in valores[i]:
                            infoHospital['leitos_disponiveis'] = 0
                        else:
                            infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                                valorHospital[2]
                        infoHospital['pacientes_covid'] = valorHospital[3]
                    elif valores[i]['R'] == 16:
                        infoHospital['leitos_ativos'] = valorHospital[2]
                        infoHospital['leitos_ocupados'] = valorHospital[3]
                        infoHospital['leitos_disponiveis'] = valorHospital[2] - \
                            valorHospital[3]
                        infoHospital['pacientes_covid'] = valorHospital[5]
                    elif valores[i]['R'] == 18:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['pacientes_covid'] = valorHospital[4]
                    elif valores[i]['R'] == 34:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[3]
                        infoHospital['pacientes_covid'] = valorHospital[4]
                    elif valores[i]['R'] == 48:
                        infoHospital['leitos_ativos'] = valorHospital[2]
                        infoHospital['leitos_ocupados'] = valorHospital[3]
                        infoHospital['leitos_disponiveis'] = valorHospital[2] - \
                            valorHospital[3]
                        if 'Ø' in valores[i]:
                            infoHospital['pacientes_covid'] = 0
                        else:
                            infoHospital['pacientes_covid'] = valorHospital[4]
                    elif valores[i]['R'] == 50:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[1]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        if 'Ø' in valores[i]:
                            infoHospital['pacientes_covid'] = -1
                        else:
                            infoHospital['pacientes_covid'] = valorHospital[3]
                    elif valores[i]['R'] == 62:
                        valorHospital = valores[i-1]['C']
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[1]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['pacientes_covid'] = -1
                    elif valores[i]['R'] == 66:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['pacientes_covid'] = -1
                    elif valores[i]['R'] == 70:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[2]
                        infoHospital['pacientes_covid'] = -1
                    elif valores[i]['R'] == 74:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[2]
                        infoHospital['pacientes_covid'] = valorHospital[1] - \
                            valorHospital[2]
                    elif valores[i]['R'] == 114:
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['pacientes_covid'] = -1
                    elif valores[i]['R'] == 126:
                        valorHospital = valores[i-1]['C']
                        infoHospital['leitos_ativos'] = valorHospital[1]
                        infoHospital['leitos_ocupados'] = valorHospital[2]
                        infoHospital['leitos_disponiveis'] = valorHospital[1] - \
                            valorHospital[2]
                        infoHospital['pacientes_covid'] = 14
                    else:
                        raise Exception("!-- Erro processando: ", i, ";", hospitais[i], ";",
                                        valorHospital, ";", valores[i]['R'])
                        break
                    # print(i, ";", hospitais[i], ";",
                    #       valorHospital, ";", valores[i]['R'])

                infoHospital['taxa_ocupacao'] = infoHospital['leitos_disponiveis'] / \
                    infoHospital['leitos_ativos']

                leitos[tipo][i] = dict(
                    hospital=infoHospital['hospital'],
                    municipio=infoHospital['municipio'],
                    index_regional=infoHospital['index_regional'],
                    leitos_ativos=infoHospital['leitos_ativos'],
                    leitos_ocupados=infoHospital['leitos_ocupados'],
                    leitos_disponiveis=infoHospital['leitos_disponiveis'],
                    taxa_ocupacao=infoHospital['taxa_ocupacao'],
                    pacientes_covid=infoHospital['pacientes_covid'],
                    dataAtualizacao=dataAtualizacao
                )

                # print(i, ",", end='', flush=True)
                print(infoHospital['hospital'], ";", infoHospital['leitos_ativos'], ";",
                      infoHospital['leitos_ocupados'], ";", infoHospital['leitos_disponiveis'], ";", valores[i])
            print("Ok")

        for tipo in range(1, 3):
            if tipo == 1:
                print("Somando o total dos leitos COVID apenas Adulto... ",
                      end='', flush=True)
            if tipo == 2:
                print("Somando o total dos leitos GERAL apenas Adulto... ",
                      end='', flush=True)
            somaAtivos = 0
            somaOcupados = 0
            somaDisponiveis = 0
            for i in leitos[tipo]:
                somaAtivos += leitos[tipo][i]['leitos_ativos']
                somaOcupados += leitos[tipo][i]['leitos_ocupados']
                somaDisponiveis += leitos[tipo][i]['leitos_disponiveis']
            print("Ok")
            if somaAtivos != totais[0]:
                raise Exception(
                    "!--- Leitos Totais não fecha {encontrado:", somaAtivos, ", deveria ser: ", totais[0], "} ---!")
            if somaOcupados != totais[1]:
                raise Exception(
                    "!--- Leitos Ocupados não fecha {encontrado:", somaOcupados, ", deveria ser: ", totais[1], "} ---!")
            if somaDisponiveis != totais[2]:
                raise Exception(
                    "!--- Leitos Disponíveis não fecha {encontrado:", somaDisponiveis, ", deveria ser: ", totais[2], "} ---!")
        if simulacao == 1:
            return
        try: 
            for tipo in range(1, 3):
                if tipo == 1:
                    print("Importando os leitos COVID apenas Adulto... ",
                        end='', flush=True)
                if tipo == 2:
                    print("Importando os leitos GERAL apenas Adulto... ",
                        end='', flush=True)
                for i in leitos[tipo]:
                    params = (
                        "NULL",
                        leitos[tipo][i]['hospital'],
                        "NULL",
                        leitos[tipo][i]['municipio'],
                        "NULL",
                        leitos[tipo][i]['index_regional'],
                        leitos[tipo][i]['leitos_ativos'],
                        leitos[tipo][i]['leitos_ocupados'],
                        leitos[tipo][i]['leitos_disponiveis'],
                        leitos[tipo][i]['taxa_ocupacao'],
                        leitos[tipo][i]['pacientes_covid'],
                        leitos[tipo][i]['dataAtualizacao']
                    )
                    if tipo == 1:
                        dadosDao.leitos_Gerais_Covid(params)
                        # (infoHospital['hospital'], ";", infoHospital['leitos_ativos'], ";",
                        #      infoHospital['leitos_ocupados'], ";", infoHospital['leitos_disponiveis'])
                    if tipo == 2:
                        dadosDao.leitos_Covid(params)
                        # print(i, ",", end='', flush=True)
                        # print(infoHospital['hospital'], ";", infoHospital['leitos_ativos'], ";",
                        #      infoHospital['leitos_ocupados'], ";", infoHospital['leitos_disponiveis'])

                '''
                        if leitos.get(infoHospital['index_regional']) == None:
                            leitos(infoHospital['index_regional']) = {
                            'regional': tabelas.getRegionalMunicipioBrasil(codigo_ibge_municipio),
                            'populacao': Utils.convert_to_int(value['populacaoTCU2019']),
                            'datas': {}}
                            '''
        except Exception as mensagem:
            print("Erro: ", mensagem)
        
        print("Ok")
