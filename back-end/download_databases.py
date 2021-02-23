import urllib.request
import json
import requests
#from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib

#teste...2223  
url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral'

#headers = CaseInsensitiveDict()

headers = {
    'authority':'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
    'accept': 'application/json, text/plain, */*' ,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)' ,
    'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm',
    'origin': 'https://covid.saude.gov.br',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://covid.saude.gov.br/',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

req_DB = requests.get(url,headers=headers).text

# data = urllib.request.urlopen(url).read()

data_DB = json.loads(req_DB)

filename = data_DB['results'][0]['texto_rodape'][:-14]+'.csv'
# print(filename)

print("Baixando base de dados do MS...\n")
url_csv = requests.get(data_DB['results'][0]['arquivo']['url'])

with open(filename,'wb') as s:
    s.write(url_csv.content) 
 
print('Base de dados do Ministério da Saúde baixado!!!\n')
    
    # URL, HEADERS para base de dados de leitos do estado (não está funcionando)
        # url_leitos = 'https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true'

        # headers_leitos = {
        #     'Accept':'application/json, text/plain, */*',
        #     'Accept-Encoding':'gzip, deflate, br',
        #     'Accept-Language':'en-US,en;q=0.9',
        #     'ActivityId':'a326e385-7373-aea8-e910-e5d5e787735a',
        #     'Connection':'keep-alive',
        #     'Content-Length':'1561',
        #     'Content-Type':'application/json;charset=UTF-8',
        #     'Host':'wabi-brazil-south-api.analysis.windows.net',
        #     'Origin':'https://app.powerbi.com',
        #     'Referer':'https://app.powerbi.com/',
        #     'RequestId':'e6a55f2d-fcae-4ca7-29f8-e0093bdee3a7',
        #     'Sec-Fetch-Dest':'empty',
        #     'Sec-Fetch-Mode':'cors',
        #     'Sec-Fetch-Site':'cross-site',
        #     'Sec-GPC': '1',
        #     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
        #     'X-PowerBI-ResourceKey':'1807b851-3dab-4963-bb2f-94f60ffc8ccc'
        # }

        # params = {
        #     'RequestId': '550b96da-6fb5-ec70-c2d2-bc1673dcdf77'
        # }

# req_leitos = requests.session()

# url_leitos = 'https://elastic-leitos.saude.gov.br/leito_ocupacao/_search?scroll=1m'

# body = {"size": 500,"query": {"match": {"estadoSigla": "SC"}}}

#url_leitos = 'https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true'

#head_leitos_req = {
    #'authority': 'elastic-leitos.saude.gov.br',
    #'method': 'GET',
    #'path': '/leito_ocupacao/_search',
    #'scheme': 'https',
    #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #'accept-encoding': 'gzip, deflate, br',
    #'accept-language': 'en-US,en;q=0.9',
    #'authorization': 'Basic dXNlci1hcGktbGVpdG9zOmFRYkxMM1pTdGFUcjM4dGo=',
    #'cookie': 'routecloud=1610045984.248.21073.235440',
    #'sec-fetch-dest': 'document',
    #'sec-fetch-mode': 'navigate',
    #'sec-fetch-site': 'none',
    #'sec-fetch-user': '?1',
    #'sec-gpc': '1',
    #'upgrade-insecure-requests': '1',
    #'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36'
#}

#resp_leitos = {
    #'content-encoding': 'gzip',
    #'content-type': 'application/json; charset=UTF-8',
    #'date': 'Fri, 05 Feb 2021 02:41:46 GMT',
    #'server': 'nginx/1.17.10',
    #'strict-transport-security': 'max-age=15724800; includeSubDomains',
    #'vary': 'Accept-Encoding'
#}

#print("Baixando DB de leitos...\n")
#req_DB_leitos = req_leitos.get(url_leitos,auth=('user-api-leitos','aQbLL3ZStaTr38tj'),data=body).text

#data_leitos = json.loads(req_DB_leitos)
#print(data_leitos,"\n")

#with open('leitos.json','w') as leitos:
    #leitos.write(req_DB_leitos) 

#print('Download da DB de leitos completo!!!\n')
