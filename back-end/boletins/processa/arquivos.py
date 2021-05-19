import urllib.request
import csv
import datetime


class arquivos:
    def getFile(url):
        file_name = url.split('epidemiologico-')[-1]
        try:
            u = urllib.request.urlopen(url)
        except:
            print("!!Erro baixando: " + file_name)
            return

        f = open("boletins/"+file_name, 'wb')
        file_size = u.length

        print ("Downloading: ",file_name," Bytes: ", file_size) 

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
                if item['dados'] == None: continue
                for itemData in item['dados']:
                    if itemData == None: continue
                    # print(itemData['regional'])
                    cabecalho1.extend([itemData['regional'] + "- Total", '', '', '' ])
                    cabecalho1.extend([itemData['regional'] + "- Adulto", '', '', '' ])
                    cabecalho2.extend(['ativos', 'ocupados_covid', 'ocupados_outros', 'livres' ])
                    cabecalho2.extend(['ativos', 'ocupados_covid', 'ocupados_outros', 'livres' ])
                break

            writer.writerow(cabecalho1)
            writer.writerow(cabecalho2)
            print("Ok")
            
            print("Gravando os dados no arquivo CSV... ")
            for itemData in dados:
                dadosDia = []
                dadosDia.append(itemData['data'].strftime('%d/%m/%Y'))
                print("-->" + itemData['data'].strftime('%d/%m/%Y'), flush=True)
                if itemData['dados'] == None: continue
                for item in itemData['dados']:
                    if item == None: continue

                    dadosDia.append(item['total']['ativos'])
                    dadosDia.append(item['total']['ocupados_covid'])
                    dadosDia.append(item['total']['ocupados_outros'])
                    dadosDia.append(item['total']['livres'])

                    dadosDia.append(item['adulto']['ativos'])
                    dadosDia.append(item['adulto']['ocupados_covid'])
                    dadosDia.append(item['adulto']['ocupados_outros'])
                    dadosDia.append(item['adulto']['livres'])
                
                # print(dadosDia)
                writer.writerow(dadosDia)
