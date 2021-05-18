import urllib.request

class download:
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