import datetime

from io import StringIO
import os.path

import tabula

from processa.processa import processa
from processa.download import download

def geraDatas():
    downloadObj = download()

    # strBase = "http://www.coronavirus.sc.gov.br/wp-content/uploads/{0}/{1:02d}/boletim-epidemiologico-{2:02d}-{1:02d}-{0}.pdf"
    strBase = "{2:02d}-{1:02d}-{0}.pdf"
    # data_inicio = datetime.datetime(2020, 4, 21, 0, 0)
    data_inicio = datetime.datetime(2021, 3, 3, 0, 0)
    data_fim = datetime.datetime.today()
    for n in range(int((data_fim - data_inicio).days)):
        data_boletim = data_inicio + datetime.timedelta(n)
        strOut = strBase.format(data_boletim.year, data_boletim.month, data_boletim.day)
        classificaPdf(strOut)
        # download.getFile(strOut)


def classificaPdf(file_path):
    if not os.path.isfile("boletins/"+file_path):
        return
    area =  (134, 50, 192, 550)
    try:
        df = tabula.read_pdf("boletins/"+file_path, output_format="json", 
            pages=[4, 7, 10, 11], 
            area=area)
        if df[0]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                df[0]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)" :
            print(file_path, "; 4 ;", df[0]['data'][0][0]['text'])
        elif df[1]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                df[1]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)" :
            print(file_path, "; 7 ;", df[1]['data'][0][0]['text'])
        elif df[2]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                df[2]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)" :
            print(file_path, "; 10 ;", df[2]['data'][0][0]['text'])
        elif df[3]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                df[3]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)" :
            print(file_path, "; 11 ;", df[3]['data'][0][0]['text'])
        else:
            print(file_path, "; Não localizado ;")
    except:
        print("!!Erro abrindo arquivo: " + file_path)
        return


    # reader = PyPDF2.PdfFileReader(file_path)
if __name__ == "__main__":
    # getFile()

    # getRegionais("http://www.coronavirus.sc.gov.br/wp-content/uploads/2021/03/boletim-epidemiologico-21-03-2021.pdf")
    geraDatas()

    #  casos_municipios = {}
    
    # casos_municipios[codigo_ibge_municipio] = {
    #                     'regional': tabelas.getRegionalMunicipioBrasil(codigo_ibge_municipio),
    #                     'populacao': Utils.convert_to_int(value['populacaoTCU2019']),
    #                     'datas': {}}
    #  casos_municipios[codigo_ibge_municipio]['datas'][key] = dict(
    #                         casos=0,
    #                         # obitos=0,
