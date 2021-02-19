import json, csv
import datetime

with open("leitos.json", 'r') as leitos:
    data_leitos = json.load(leitos)

dt_leitos = []

# print(data_leitos['hits']['hits'][4])

for m in data_leitos['hits']['hits']:
    
    try:
        estado = m['_source']['estado'];
    except ValueError as ex:
        estado = None;

    try:
        estadoSigla = m['_source']['estadoSigla'];
    except ValueError as ex:
        estadoSigla = None;

    try:
        municipio = m['_source']['municipio'];
    except ValueError as ex:
        municipio = None;

    try:
        cnes = m['_source']['cnes'];
    except ValueError as ex:
        cnes = None;

    try:
        nomeCnes = m['_source']['nomeCnes'];
    except KeyError as ex:
        nomeCnes = None;

    try:
        dataNotificacaoOcupacao = m['_source']['dataNotificacaoOcupacao'][:-14]
    except ValueError as ex:
        dataNotificacaoOcupacao = None;

    try:
        ofertaRespiradores = m['_source']['ofertaRespiradores'];
    except KeyError as ex:
        ofertaRespiradores = None;

    try:
        ofertaHospCli = m['_source']['ofertaHospCli'];
    except KeyError as ex:
        ofertaHospCli = None;

    try:
        ofertaHospUti = m['_source']['ofertaHospUti'];
    except KeyError as ex:
        ofertaHospUti = None;

    try:
        ofertaSRAGCli = m['_source']['ofertaSRAGCli'];
    except KeyError as ex:
        ofertaSRAGCli = None;

    try:
        ofertaSRAGUti = m['_source']['ofertaSRAGUti'];
    except KeyError as ex:
        ofertaSRAGUti = None;

    try:
        ocupHospCli = m['_source']['ocupHospCli'];
    except ValueError as ex:
        ocupHospCli = None;

    try:
        ocupHospUti = m['_source']['ocupHospUti'];
    except ValueError as ex:
        ocupHospUti = None;

    try:
        ocupSRAGCli = m['_source']['ocupSRAGCli'];
    except ValueError as ex:
        ocupSRAGCli = None;

    try:
        ocupSRAGUti = m['_source']['ocupSRAGUti'];
    except ValueError as ex:
        ocupSRAGUti = None;

    try:
        altas = m['_source']['altas'];
    except ValueError as ex:
        altas = None;

    try:
        obitos = m['_source']['obitos'];
    except ValueError as ex:
        obitos = None;

    try:
        ocupacaoInformada = m['_source']['ocupacaoInformada'];
    except ValueError as ex:
        ocupacaoInformada = None;

    try:
        algumaOcupacaoInformada = m['_source']['algumaOcupacaoInformada'];
    except ValueError as ex:
        algumaOcupacaoInformada = None;

    dt_leitos.append(dict(
        estado=estado,
        estadoSigla= estadoSigla,
        municipio= municipio,
        cnes= cnes,
        nomeCnes= nomeCnes,
        dataNotificacaoOcupacao= dataNotificacaoOcupacao,
        ofertaRespiradores = ofertaRespiradores,
        ofertaHospCli = ofertaHospCli,
        ofertaHospUti = ofertaHospUti,
        ofertaSRAGCli = ofertaSRAGCli,
        ofertaSRAGUti = ofertaSRAGUti,
        ocupHospCli = ocupHospCli,
        ocupHospUti = ocupHospUti,
        ocupSRAGCli = ocupSRAGCli,
        ocupSRAGUti = ocupSRAGUti,
        altas = altas,
        obitos = obitos,
        ocupacaoInformada = ocupacaoInformada,
        algumaOcupacaoInformada = algumaOcupacaoInformada
    ))
    
with open('leitos.csv', 'w') as write:
    fieldnames = ['estado','estadoSigla','municipio','cnes','nomeCnes','dataNotificacaoOcupacao','ofertaRespiradores','ofertaHospCli','ofertaHospUti','ofertaSRAGCli','ofertaSRAGUti','ocupHospCli','ocupHospUti','ocupSRAGCli','ocupSRAGUti','altas','obitos','ocupacaoInformada','algumaOcupacaoInformada']
    file = csv.DictWriter(write, fieldnames=fieldnames)
    file.writeheader()

    test = [{
        "estado": "Santa Catarina",
                    "estadoSigla": "SC",
                    "municipio": "Penha",
                    "cnes": "2691469",
                    "nomeCnes": "HOSPITAL DE PENHA",
                    "dataNotificacaoOcupacao": "2020-09-30T03:00:45.409Z",
                    "ofertaRespiradores": 1,
                    "ofertaHospCli": 28,
                    "ofertaHospUti": 0,
                    "ofertaSRAGCli": 20,
                    "ofertaSRAGUti": 0,
                    "ocupHospCli": 0,
                    "ocupHospUti": 0,
                    "ocupSRAGCli": 0,
                    "ocupSRAGUti": 0,
                    "altas": 0,
                    "obitos": 0,
                    "ocupacaoInformada": "true",
                    "algumaOcupacaoInformada": "true"
    },
    {
        "estado": "Santa Catarina",
                    "estadoSigla": "SC",
                    "municipio": "Taió",
                    "cnes": "2377616",
                    "nomeCnes": "HOSPITAL E MATERNIDADE DONA LISETTE",
                    "dataNotificacaoOcupacao": "2020-09-20T03:00:00.000Z",
                    "ofertaRespiradores": 0,
                    "ofertaHospCli": 37,
                    "ofertaHospUti": 0,
                    "ofertaSRAGCli": 0,
                    "ofertaSRAGUti": 0,
                    "ocupHospCli": 4,
                    "ocupHospUti": 0,
                    "ocupSRAGCli": 0,
                    "ocupSRAGUti": 0,
                    "altas": 0,
                    "obitos": 0,
                    "ocupacaoInformada": "true",
                    "algumaOcupacaoInformada": "true"
    }]

    file.writerows(dt_leitos)

