import urllib.request
import csv
import datetime
import os.path


class arquivos:
    def getFile(url):
        file_name = url.split('epidemiologico-')[-1]
        try:
            u = urllib.request.urlopen(url)
        except:
            print("!!Erro baixando: " + file_name)
            return

        f = open(
            "/Users/marcelocendron/Dropbox/web/subcomite/back-end/boletins/boletins/" + file_name, 'wb')
        file_size = u.length

        print("Downloading: ", file_name, " Bytes: ", file_size)

        f.write(u.read())
        f.close()

    def salvaCSV(_self, dados):
        filename = 'leitos.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            cabecalho1 = ["data"]
            cabecalho2 = [""]
            print("Gerando cabeçalho do CSV... ", end='', flush=True)

            for item in dados:
                if item['dados'] == None:
                    continue
                for itemData in item['dados']:
                    if itemData == None:
                        continue
                    # print(itemData['regional'])
                    cabecalho1.extend(
                        [itemData['regional'] + "- Total", '', '', ''])
                    cabecalho1.extend(
                        [itemData['regional'] + "- Adulto", '', '', ''])
                    cabecalho2.extend(
                        ['ativos', 'ocupados_covid', 'ocupados_outros', 'livres'])
                    cabecalho2.extend(
                        ['ativos', 'ocupados_covid', 'ocupados_outros', 'livres'])
                break

            writer.writerow(cabecalho1)
            writer.writerow(cabecalho2)
            print("Ok")

    def salvaCSVLeitos(_self, dados):
        filename = 'filaLeitos.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            cabecalho1 = ["data"]
            print("Gerando cabeçalho do CSV... ", end='', flush=True)

            regionais = ['data',
                         'GRANDE OESTE - CHAPECÓ',
                         'MEIO OESTE - JOAÇABA',
                         'SERRA - LAGES',
                         'NORTE - JOINVILLE',
                         'VALE - BLUMENAU',
                         'FOZ - ITAJAÍ',
                         'SUL - CRICIÚMA',
                         'GRANDE FLORIANÓPOLIS']
            writer.writerow(regionais)

            print("Ok")

            print("Gravando os dados no arquivo CSV... ")
            for itemData in dados:
                dadosDia = itemData['dados']
                if dadosDia == None:
                    continue
                dadosDia.insert(0, itemData['data'].strftime('%d/%m/%Y'))
                # print(dadosDia)
                writer.writerow(dadosDia)
