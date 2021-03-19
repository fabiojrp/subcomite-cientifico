import urllib.request
import json
import requests
# from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib

url = ' https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true'

# headers = CaseInsensitiveDict()

headers = {
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

data = {"version": "1.0.0", "queries": [{"Query": {"Commands": [{"SemanticQueryDataShapeCommand": {"Query": {"Version": 2, "From": [{"Name": "f", "Entity": "fat_leitos_hospitalares", "Type": 0}, {"Name": "#", "Entity": "#Medidas 1 - Quantitativos Gerais", "Type": 0}, {"Name": "d", "Entity": "dim_macrorregioes", "Type": 0}], "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "hospital"}, "Name": "fat_leitos_hospitalares.hospital"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ativos"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ativos"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Ocupados"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Ocupados"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Leitos Disponíveis"}, "Name": "#Medidas 1 - Quantitativos Gerais.Leitos Disponíveis"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Taxa de Ocupação"}, "Name": "#Medidas 1 - Quantitativos Gerais.Taxa de Ocupação"}, {"Measure": {"Expression": {"SourceRef": {"Source": "#"}}, "Property": "Pacientes COVID Internados"},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          "Name": "#Medidas 1 - Quantitativos Gerais.{GAL} Internados COVID (Conf&Susp)"}, {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}, "Name": "dim_macrorregioes.macro_desc_ac"}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "Leito COVID 2"}}], "Values": [[{"Literal": {"Value": "'COVID'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "classificacao"}}], "Values": [[{"Literal": {"Value": "'uti'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_tipo"}}], "Values": [[{"Literal": {"Value": "'ADULTO'"}}]]}}}, {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "leito_sus"}}], "Values": [[{"Literal": {"Value": "true"}}]]}}}], "OrderBy": [{"Direction": 1, "Expression": {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "macro_desc_ac"}}}]}, "Binding": {"Primary": {"Groupings": [{"Projections": [0, 1, 2, 3, 4, 5, 6], "Subtotal":1}]}, "DataReduction":{"DataVolume": 3, "Primary": {"Window": {"Count": 500}}}, "Version": 1}}}]}, "QueryId": "", "ApplicationContext": {"DatasetId": "0c400f04-4bb2-4414-867e-790bdd9dcd5f", "Sources": [{"ReportId": "e585da1e-bcb4-46d8-ad92-6dc8640f59ed"}]}}], "cancelQueries": [], "modelId": 2604433}
req_DB = requests.post(url, headers=headers, json=data).text

# data = urllib.request.urlopen(url).read()

data_DB = json.loads(req_DB)

print(data_DB)
