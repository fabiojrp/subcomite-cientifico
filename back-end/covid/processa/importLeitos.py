from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pandas import ExcelWriter

# from covid.processa.processaLeitos import processaLeitos
# from covid.processa.dados.Utils import Utils
# from covid.processa.dao.DadosDao import DadosDao
# from covid.processa.db.create import Create

import time
import datetime
import pandas as pd

"""
A execução script precisa que o webdrive do Chrome seja instalado, para
que o Selenium possa simular a entrada no site.

Para isso é necessário instalar o webdrive apropriado para cada SO, ver em:
https://www.selenium.dev/documentation/en/selenium_installation/installing_webdriver_binaries/

O <endereço> de constar na seguinte linha de código webdrive.Chrome(..., executable_path='<endereço>')
"""


class importLeitos:
    def __init__(self, simulacao=0):
        print("initing....")
        # create = Create()
        # create.create_leitos()
        # self.dadosDao = DadosDao()

    def getData(self, tipo="Geral"):
        try:
            # Objeto com configurações do Chrome
            self.options = webdriver.ChromeOptions()
            # Para não abrir a janela do browser
            self.options.headless = True
            # Para iniciar com janela maximizada (não precisa neste problema)
            # self.options.add_argument("start-maximized")

            # Inicia o driver baseado nas opções e no path do webdriver
            self.driver = webdriver.Chrome(
                options=self.options, executable_path=r'/Users/marcelocendron/Downloads/chromedriver')

            # self.driver = webdriver.Chrome(
            #     options=self.options, executable_path=r'/home/usuario/subcomite-cientifico/back-end/covid/processa/chromedriver')
            self.driver.get("https://app.powerbi.com/view?r=eyJrIjoiMTgwN2I4NTEtM2RhYi00OTYzLWJiMmYtOTRmNjBmZmM4Y2NjIiwidCI6ImExN2QwM2ZjLTRiYWMtNGI2OC1iZDY4LWUzOTYzYTJlYzRlNiJ9&pageName=ReportSectiona4ec0366fe4acb30c1b7")
            wait = WebDriverWait(self.driver, 30)

            # Obtemos o slicer-dropdown-menu de Tipos de Leito
            xpath = "//div[@aria-label='Tipo de Leito,  All']"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            dropdown_menu = self.driver.find_element_by_xpath(xpath)
            dropdown_menu.click()
            # Obtemos a opção ADULTO que aparecere por conta desse dropown
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@aria-label='ADULTO']")))
            dropdown_item = self.driver.find_element_by_xpath(
                "//div[@aria-label='ADULTO']")
            dropdown_item.click()
            # Escondemos o menu clicando novamente nele
            dropdown_menu.click()

            # Obtemos o slicer-dropdown-menu de Leito COVID / GERAL
            xpath = "//div[@aria-label='Leito COVID / GERAL,  All']"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            dropdown_menu = self.driver.find_element_by_xpath(xpath)
            dropdown_menu.click()

            if tipo == "Covid":
                # Obtemos a opção COVID que aparecere por conta desse dropown
                xpath = "//div[@aria-label='COVID']"
                wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                dropdown_item = self.driver.find_element_by_xpath(xpath)
                dropdown_item.click()
                # Escondemos o menu clicando novamente nele
                dropdown_menu.click()

            # xpath = "//div[@title='Macroregião']"
            # wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            xpath = "//div[@class='bodyCells']"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("document.querySelector('div[class=\"bodyCells\"]').scrollTo(0, 600)")
            self.driver.execute_script("document.querySelector('div[class=\"bodyCells\"]').click()")
            # self.driver.implicitly_wait(40) # seconds
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            # Extraimos o código html e usamos BeautifulSoup (muito útil para achar conteúdo no DOM)
            htmlSource = self.driver.page_source
            soup = BeautifulSoup(htmlSource, 'html.parser')

            return soup

        except Exception as mensagem:
            print("Erro: ", mensagem)
        finally:
            self.driver.quit()


    def processData(self, soup, tipo):

        # with open("/Users/marcelocendron/Downloads/01.html", "w") as file:
        #     file.write(str(bodyCells))

        data = soup.find('tspan')
        dataAtualizacao = datetime.datetime.strptime(
            data.text, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")

        totalSoup = soup.find('div', {'class': 'floatingBodyCells'})
        divTotalSoup = totalSoup.findChildren(
            'div', {'class': 'pivotTableCellWrap'})
        totais = {'leitos_ativos': 0,
                  'leitos_ocupados': 0,
                  'leitos_disponiveis': 0}

        totais['leitos_ativos'] = int(divTotalSoup[2].text.replace(",", ""))
        totais['leitos_ocupados'] = int(divTotalSoup[3].text.replace(",", ""))
        totais['leitos_disponiveis'] = int(
            divTotalSoup[4].text.replace(",", ""))

        # totalSoup2 = soup.find('div', {'class': 'tableExContainer'})

        # Esta é a DIV que contém a tabela
        bodyCells = soup.find('div', 'bodyCells')
        # A tabela de dados é o primeiro filho de de bodyCells
        div_table = bodyCells.findChildren("div", recursive=False)[0]
        # Dentro da tabela pode ter várias páginas de dados
        div_pages = div_table.findChildren("div", recursive=False)

        tableExContainer = soup.find('div', 'tableExContainer')
        with open("/Users/marcelocendron/Downloads/01.html", "w") as file:
             file.write(str(tableExContainer))   

        list_list_list = []
        # Para página da tabela
        for div_page in div_pages:
            columns_page = div_page.findChildren("div", recursive=False)
            list_list = []
            # Para cada coluna da tabela
            for column in columns_page:
                rows = column.findChildren("div", recursive=False)
                list = []
                # Para cada linha da coluna
                for row in rows:
                    list.append(row.text)

                list_list.append(list)
            list_list_list.append(list_list)

        # for listHospitais in list_list_list:
        #     # print(list_list[0])
        #     for i in range(0, len(listHospitais[0])):
        #         infoHospital = processaLeitos.buscaInfoHospital(
        #             listHospitais[1][i])
        #         if infoHospital == -1:
        #             break

        #         infoHospital['hospital'] = listHospitais[1][i]
        #         infoHospital['leitos_ativos'] = Utils.convert_to_int(
        #             listHospitais[2][i])
        #         infoHospital['leitos_ocupados'] = Utils.convert_to_int(
        #             listHospitais[3][i])
        #         infoHospital['leitos_disponiveis'] = Utils.convert_to_int(
        #             listHospitais[4][i])
        #         infoHospital['taxa_ocupacao'] = Utils.convert_to_int(
        #             listHospitais[5][i])
        #         infoHospital['pacientes_covid'] = Utils.convert_to_int(
        #             listHospitais[6][i])
        #         # print(infoHospital)
        #         params = (
        #             "NULL",
        #             infoHospital['hospital'],
        #             "NULL",
        #             infoHospital['municipio'],
        #             "NULL",
        #             infoHospital['index_regional'],
        #             infoHospital['leitos_ativos'],
        #             infoHospital['leitos_ocupados'],
        #             infoHospital['leitos_disponiveis'],
        #             infoHospital['taxa_ocupacao'],
        #             infoHospital['pacientes_covid'],
        #             dataAtualizacao
        #         )
        #         # print(params)
        #         if tipo == "Geral":
        #             # self.dadosDao.leitos_Gerais_Covid(params)
        #             (infoHospital['hospital'], ";", infoHospital['leitos_ativos'], ";",
        #              infoHospital['leitos_ocupados'], ";", infoHospital['leitos_disponiveis'])
        #         if tipo == "Covid":
        #             # self.dadosDao.leitos_Covid(params)
        #             #     # print(i, ",", end='', flush=True)
        #             print(infoHospital['hospital'], ";", infoHospital['leitos_ativos'], ";",
        #                   infoHospital['leitos_ocupados'], ";", infoHospital['leitos_disponiveis'])

        # transforma o array de 3 dimensões list_list_list
        # em um DataFrame
        df = pd.DataFrame()
        for list_list in list_list_list:
            df_page = pd.DataFrame(list_list).transpose()
            df = pd.concat([df, df_page]).reset_index(drop=True)
        # # Colocamos os nomes das colunas (em outra implementação podemos trazer eles do DOM)
        df.columns = ['macrorregiao', 'hospital', 'leitos_ativos', 'leitos_ocupados',
                      'leitos_disponiveis', 'taxa_ocupacao', 'pacientes_covid']

        with ExcelWriter('dados.xlsx') as writer:
            df.to_excel(writer, sheet_name='df')

        #  converte os valores para números
        df['leitos_ativos'] = pd.to_numeric(
            df['leitos_ativos'], errors='coerce', downcast='integer')
        df['leitos_ocupados'] = pd.to_numeric(
            df['leitos_ocupados'], errors='coerce', downcast='integer')
        df['leitos_disponiveis'] = pd.to_numeric(
            df['leitos_disponiveis'], errors='coerce', downcast='integer')

        # Verifica se os valores estão fechando:
        for valor in totais:
            print("Total {0}, BD: {1}".format(totais[valor], df[valor].sum()))

        # if somaAtivos != totais[0]:
        #     raise Exception(
        #         "!--- Leitos Totais não fecha {encontrado:", somaAtivos, ", deveria ser: ", totais[0], "} ---!")

# CREATE TABLE IF NOT EXISTS public.leitosgeraiscovid
# (
#     macrorregiao character varying(100) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
#     hospital character varying(100) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
#     municipio character varying(100) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
#     codigo_ibge_municipio integer,
#     regional_saude character varying(100) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
#     index_regional integer,
#     leitos_ativos integer,
#     leitos_ocupados integer,
#     leitos_disponiveis integer,
#     taxa_ocupacao numeric(5,2) DEFAULT NULL::numeric,
#     pacientes_covid integer,
#     atualizacao timestamp without time zone
# )

        # Mostramos dataset
        print(df)

        # # Salvamos o DataFrame em um arquivo usando o horário atual
        # timestr = time.strftime("%Y%m%d-%H%M%S")
        # df.to_csv('sc/' + timestr + '.csv', index=False)

        # Neste local teria que escrever na tabela do banco de dados em postgres


if __name__ == "__main__":
    importLeitos = importLeitos()
    print("Leitos Gerais ...")
    soupData = importLeitos.getData("Geral")
    importLeitos.processData(soupData, "Geral")

    print("\nApenas Leitos  Covid...")
    soupData = importLeitos.getData("Covid")
    importLeitos.processData(soupData, "Covid")
