import csv
import datetime
from RT.processaBD import processaDB
from RT.processaDados import processaDados
from dados import tabelas

processaDB = processaDB()
processaDB.create_table()

processaDados = processaDados()

index = 0
with open('RtSC.xlsx - site.csv', 'r', encoding='utf-8-sig') as arquivo:
    dados = csv.DictReader(arquivo, delimiter=",")
    header = dados.fieldnames
    print("Inserindo os dados de RT: ", end='', flush=True)
    for value in dados:

        regiaoSaude = processaDados.buscaRegiao(value['Região da Saúde'])
        if regiaoSaude == -1:
            break

        for v in value:
            print(v)
            if v == 'Região da Saúde':
                continue
            if v == 'Instituto Federal Catarinense':
                continue
            valorRT = str(value[v].replace(',', '.'))
            if valorRT:
                dadosSql = [regiaoSaude,
                            processaDados.date_format(v),
                            valorRT
                            ]
                processaDB.insert_value_rt(dadosSql)
            else:
                dadosSql = [regiaoSaude,
                            processaDados.date_format(v)
                            ]
                processaDB.insert_value_rt2(dadosSql)
            index = index + 1
            if index % 100 == 0:
                print('.', end='', flush=True)

    print("\nFeito")
