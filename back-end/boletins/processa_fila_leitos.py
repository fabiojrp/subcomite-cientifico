import datetime

from io import StringIO
import os.path

import tabula

from processa.extrair import extrair
from processa.arquivos import arquivos


def getDados():
    arquivosObj = arquivos()

    strBase = "{2:02d}-{1:02d}-{0}.pdf"
    data_inicio = datetime.datetime(2021, 3, 3, 0, 0)
    data_fim = datetime.datetime.today()
    # data_fim = datetime.datetime(2021, 3, 10, 0, 0)

    dados = []
    for n in range(int((data_fim - data_inicio).days)):
        data_boletim = data_inicio + datetime.timedelta(n)
        strOut = strBase.format(
            data_boletim.year, data_boletim.month, data_boletim.day)
        dados.append({
            'data': data_boletim,
            'dados': extraiDadosLeitosPdf(strOut)
        })
        # print(dados)
        # arquivos.getFile(strOut)

    arquivosObj.salvaCSVLeitos(dados)


def extraiDadosLeitosPdf(file_path):
    extrairObj = extrair()
    print("-->Arquivo: "+file_path)
    file_path = os.path.dirname(__file__)+"/boletins/"+file_path
    if not os.path.isfile(file_path):
        return
    area = (130, 120, 160, 480)
    try:
        df = tabula.read_pdf(file_path, output_format="json",
                             pages=[9],
                             area=area)
        if df[0]['data']:
            if df[0]['data'][0][0]['text'].strip() == "SOLICITAÇÕES DE TRANSFERÊNCIA":
                dadosRegionais = extrairObj.getFilaLeitos(
                    file_path, 9)
                return dadosRegionais
                print(file_path, "; Tem dados, mas não localizou a texto ;")

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
