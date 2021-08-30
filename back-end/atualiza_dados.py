import sys
import time
import datetime

from covid.processa.download_databases import download_databases
from covid.processa.processaCSV import processaCSV
from covid.processa.processaMunicipios import processaMunicipios
from covid.processa.importLeitos import importLeitos
from covid.processa.calculaRT import calculaRT
from covid.processa.download_vacinados import download_vacinados
from covid.processa.download_vacinados_MS import download_vacinados_MS
from covid.processa.rt_predictor.predict_store import predict_store
from covid.processa.indicadores.processaIndicadores import processaIndicadores

with open('covid.log', 'w') as f:
    # sys.stdout = f  # Change the standard output to the file we created.from covid.processa.download_leitos import download_leitos

    # processaCSV = processaCSV() 
    # processaMunicipios = processaMunicipios()
    # calculaRT = calculaRT()

    try:
        start_time = time.time()

        # # # Faz o download dos casos do site do Ministério da Saúde
        # download_databases()

        # # # # # # Lê o arquivo baixado na função anterior e retorna a tabela com o número de casos e óbitos
        # casos_municipios = processaCSV.readStoreCSVFile()

        # # # # # # # # # # Faz o processado dos dados
        # processaMunicipios.processamento(casos_municipios)

        # # # # # # # # Faz o calculo da RT para as regionais
        # calculaRT.gerarRTRegionais()

        # # Atualiza a vacinação da DIVE
        # try:
        #     dv = download_vacinados()
        #     dataDB = dv.getFile()
        #     if dataDB:
        #         df = dv.processData(dataDB)
        #         dv.storeBD(df)
        # except Exception as mensagem:
        #     print("Erro: ", mensagem)


        # # # # Baixa e processa os dados de vacinados do MS
        # try:
        #     dowVacMS = download_vacinados_MS()
        #     if dowVacMS.getFile(): 
        #         dowVacMS.processaVacinacaoMS()
        # except Exception as mensagem:
        #     print("Erro: ", mensagem)

        # # Ainda em fase de teste - Faz o download dos leitos - Método 2
        # importLeitos = importLeitos()

        # print("Leitos Gerais ...")
        # for i in range(1,6):
        #     try:
        #         print("Tentativa {0}".format(i))
        #         soupData = importLeitos.getData("Geral", i*100)
        #         df = importLeitos.processData(soupData, "Geral")
        #         importLeitos.salvaBD(df, importLeitos.param_dic, 'leitosgeraiscovid' )

        #     except Exception as mensagem:
        #         print("Erro processando dados:", mensagem)
        #         continue
        #     break


        # print("\nApenas Leitos Covid...")
        # for i in range(1,6):
        #     try:
        #         print("Tentativa {0}....".format(i))
        #         soupData = importLeitos.getData("Covid", i*100)
        #         df = importLeitos.processData(soupData, "Covid")
        #         importLeitos.salvaBD(df, importLeitos.param_dic, 'leitoscovid' )
        #         # importLeitos.salvaExcel(df)
        #     except Exception as mensagem:
        #         print("Erro processando dados:", mensagem)
        #         continue
        #     break

        # # # # Executa o script para prever o RT
        # try:
        #     predict_store()
        # except Exception as mensagem:
        #     print("Erro: ", mensagem)

        # Script para calculo dos indicadores da região. 
        processaIndicadores = processaIndicadores()
        processaIndicadores.processaIndicadoresDiario()

        # Executa apenas nas quintas, 
        # Segunda=0, Terça=1, Quarta=2, Quinta=3
        if datetime.datetime.today().weekday() == 3:
            processaIndicadores.processaIndicadoresBD()

    
        print("\n\nConcluido\n")
        print("\n--- %s seconds ---\n" % (time.time() - start_time))
    except IndexError as mensagem:
        print("Erro processando dados:", mensagem)
    except Exception as mensagem:
        print("Erro: ", mensagem)


sys.stdout = sys.stdout  # Reset the standard output to i   ts original value
