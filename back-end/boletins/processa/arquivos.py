import urllib.request
import csv

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
            for itemData in dados:
                for item in itemData['dados']:
                    
                    writer.writerow(item)
