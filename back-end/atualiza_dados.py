import sys
import time

from covid.processa.importRT import importRT
from covid.processa.download_databases import download_databases
from covid.processa.processaCSV import processaCSV
from covid.processa.processaMunicipios import processaMunicipios
from covid.processa.download_leitos import download_leitos

from covid.processa.importLeitos import importLeitos

with open('covid.log', 'w') as f:
    # sys.stdout = f  # Change the standard output to the file we created.from covid.processa.download_leitos import download_leitos

    processaCSV = processaCSV()
    processaMunicipios = processaMunicipios()

    try:
        start_time = time.time()

        # Ainda em fase de teste - Faz o download dos leitos - Método 1
        download_leitos()

        # Ainda em fase de teste - Faz o download dos leitos - Método 2
        # importLeitos = importLeitos()
        # print("Leitos Gerais ...")
        # soupData = importLeitos.getData("Geral")
        # importLeitos.processData(soupData, "Geral")

        # print("\nApenas Leitos  Covid...")
        # soupData = importLeitos.getData("Covid")
        # importLeitos.processData(soupData, "Covid")

        # Carrega os valores de RT, lembrar de incluir o arquivo RtSC.xlsx - site.csv
        importRT()

        # Faz o download dos casos do site do Ministério da Saúde
        download_databases()

        # Lê o arquivo baixado na função anterior e retorna a tabela com o número de casos e óbitos
        casos_municipios = processaCSV.readStoreCSVFile()

        # # Faz o processado dos dados
        processaMunicipios.processamento(casos_municipios)

        print("\n\nConcluido\n")
        print("\n--- %s seconds ---\n" % (time.time() - start_time))
    except IndexError as mensagem:
        print("Erro processando dados:", mensagem)
    except Exception as mensagem:
        print("Erro: ", mensagem)


sys.stdout = sys.stdout  # Reset the standard output to its original value