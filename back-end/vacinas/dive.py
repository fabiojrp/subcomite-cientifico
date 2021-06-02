import os.path
import urllib.request
from urllib.parse import quote


class dive(object):

    def getFilesPath():
        file_path = os.getcwd() + '/back-end/vacinas/arquivos_notas_tecnicas.txt'

        with open(file_path, 'r') as arquivo:
            filesPath = list(arquivo)
            filesPath = list(map(str.strip, filesPath))

        for url in filesPath:
            dive.getFile(url)

    def getFile(url):
        fullUrl = ('http://www.dive.sc.gov.br' + url).replace(' ', '%20').encode('ISO-8859-1').strip()
        try:
            u = urllib.request.urlopen(fullUrl)
            file_size = u.length
            print("Downloading: ", fullUrl, " Bytes: ", file_size)
        except:
            print("!!Erro baixando: " + fullUrl)
            return

        file_name = url.split('/')[-1]
        f = open(os.getcwd() + '/back-end/vacinas/balancos/' + file_name, 'wb')

        f.write(u.read())
        f.close()


if __name__ == "__main__":

    dive.getFilesPath()
