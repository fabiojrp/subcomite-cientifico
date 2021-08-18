import datetime
import PyPDF2 as pyPdf

from io import StringIO
import os.path

import tabula

from processa.extrair import extrair
from processa.arquivos import arquivos

"""
datetime(2020, 5, 10, 0, 0) a datetime(2020, 5, 21, 0, 0) = apenas dados do estado na página 10
datetime(2020, 5, 22, 0, 0) a datetime(2020, 7, 23, 0, 0) = Dados do estado na página 10, página 11 tem todas as regiões
datetime(2020, 7, 24, 0, 0) a datetime(2020, 9, 8, 0, 0) = Dados do estado na página 10, páginas de 11 a 14 tem as regiões
datetime(2020, 9, 9, 0, 0) a datetime(2020, 11, 23, 0, 0) = Dados do estado na página 11, páginas de 12 a 15 tem as regiões
datetime(2020, 11, 24, 0, 0) a datetime.today() = Dados do estado na página 4, páginas de 5 a 8 tem as regiões
"""

def getDados():
    arquivosObj = arquivos()

    # strBase = "http://www.coronavirus.sc.gov.br/wp-content/uploads/{0}/{1:02d}/boletim-epidemiologico-{2:02d}-{1:02d}-{0}.pdf"
    # http://www.coronavirus.sc.gov.br/wp-content/uploads/2021/05/Clique-aqui-para-acessar-o-resumo-3.pdf
    strBase = "{2:02d}-{1:02d}-{0}.pdf"

    data_inicio = datetime.datetime(2020, 5, 22, 0, 0)
    data_fim = datetime.datetime.today()
    # data_fim = datetime.datetime(2020, 11, 28, 0, 0)
    dados = []
    for n in range(int((data_fim - data_inicio).days)):
        data_boletim = data_inicio + datetime.timedelta(n)
        strOut = strBase.format(
             data_boletim.year, data_boletim.month, data_boletim.day)
        dados.append({
            'data': data_boletim,
            'dados': extraiDadosPdf(strOut)
        })
        # print(dados)

        # arquivos.getFile(strOut)

    arquivosObj.salvaCSV(dados)


def extraiDadosPdf(file_path):
    extrairObj = extrair()
    print("-->Arquivo: "+file_path)
    file_path = "boletins/"+file_path
    if not os.path.isfile(file_path):
        return
    area = (134, 50, 192, 550)
    try:
        pdf = pyPdf.PdfFileReader(open(file_path, "rb"))
        if pdf.getNumPages() <= 10:
            paginas = [4, 7, 10]
        else:
            paginas = [4, 7, 10, 11]
        df = tabula.read_pdf(file_path, output_format="json",
                             pages=paginas,
                             area=area)
        if df[0]['data']:
            if df[0]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                    df[0]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)":
                # Dados do Estado na página 4
                # dadosSC = extrairObj.getDadosSC(file_path, 4)

                # Dados das regiões nas páginas 5,6,7,8
                dadosRegionais = extrairObj.getDadosRegionais(
                    file_path, [5, 6, 7, 8])
                return dadosRegionais

        if df[1]['data']:
            if df[1]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                    df[1]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)":
                # print(file_path, "; 7 ;", df[1]['data'][0][0]['text'])
                # apenas dados do Estado na página 7
                dados = extrairObj.getDadosSC(file_path, 7) 
                return None

        if df[2]['data']:
            if df[2]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                    df[2]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)":
                # print(file_path, "; 10 ;", df[2]['data'][0][0]['text'])
                # Dados do Estado na página 10
                # dadosSC = extrairObj.getDadosSC(file_path, 10)

                dadosRegionais = None
                if df[3]['data'][1][0]['text']:
                    if df[3]['data'][1][0]['text'] == 'OCUPAÇÃO DE':
                        dadosRegionais = extrairObj.getDadosRegionais2(
                            file_path, [11])
                        return dadosRegionais

                else:
                    # Dados das regiões nas páginas 11,12,13,14
                    dadosRegionais = extrairObj.getDadosRegionais(file_path, [11, 12, 13, 14])
                    return dadosRegionais
                return None

        if df[3]['data']:
            if df[3]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (SUS E REDE PRIVADA)" or \
                    df[3]['data'][0][0]['text'].strip() == "OCUPAÇÃO DE LEITOS DE UTI (TOTAL GERAL DO SUS E REDE PRIVADA)":
                # Dados do Estado na página 11
                # dadosSC = extrairObj.getDadosSC(file_path, 11)

                # Dados das regiões nas páginas 12,13,14,15
                dadosRegionais = extrairObj.getDadosRegionais(
                    file_path, [12, 13, 14, 15])
                return dadosRegionais

        else:
            print(file_path, "; Não localizado ;")
    except Exception as e:
        print("!!!Erro!!!")
        print(e)
        print("Arquivo: " + file_path)
        return


    # reader = PyPDF2.PdfFileReader(file_path)
if __name__ == "__main__":
    getDados()

    #  casos_municipios = {}

    # casos_municipios[codigo_ibge_municipio] = {
    #                     'regional': tabelas.getRegionalMunicipioBrasil(codigo_ibge_municipio),
    #                     'populacao': Utils.convert_to_int(value['populacaoTCU2019']),
    #                     'datas': {}}
    #  casos_municipios[codigo_ibge_municipio]['datas'][key] = dict(
    #                         casos=0,
    #                         # obitos=0,
