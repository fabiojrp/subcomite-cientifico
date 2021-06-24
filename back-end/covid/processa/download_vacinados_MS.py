import os
import time
import pandas as pd
import numpy as np
import psycopg2
import json

from sqlalchemy import create_engine
from urllib.parse import quote
from datetime import datetime
from .dados.tabelas import Tabelas
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

"""
A execução script precisa que o webdrive do Chrome seja instalado, para
que o Selenium possa simular a entrada no site.

Para isso é necessário instalar o webdrive apropriado para cada SO, ver em:
https://www.selenium.dev/documentation/en/selenium_installation/installing_webdriver_binaries/

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--remote-debugging-port=9222")  # this


class download_vacinados_MS:

    def __init__(self):

        self.grupos_prioritarios = {

        }

        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "!admpasswd@covid"
        }

        self.db = self.connect()

        with open(os.getcwd() + '/back-end/covid/processa/vacinas/municipios.txt') as f:
            # with open(os.getcwd() + 'back-end/covid/processa/vacinas/municipios.txt') as f:
            self.dadosMunicipio = f.read().upper()

        # Reconstruindo a lista dos munícipios.
        self.municipios = json.loads(self.dadosMunicipio)

    def getFile(self):

        # DOWNLOAD DO ARQUIVO DE VACINAÇÃO DO MS

        # O <endereço> de constar na seguinte linha de código webdrive.Chrome(..., executable_path='<endereço>')
        path_chromedriver = os.getcwd() + '/back-end/chromedriver'

        driver = webdriver.Chrome(
            options=chrome_options, executable_path=r"{}".format(path_chromedriver))

        # A linha abaixo é bem comum, mas não teve o efeito desejado neste problema
        # Acredito que em função de que a página carrega antes e ficam requisições assíncronas em execução.
        # Por isso vamos usar time.sleep mais pra frente
        # driver.implicitly_wait(20)
        # A seguir o site específico da terceira página (aba) do dashboard

        driver.get("https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao")

        # Antes de pegar o conteúdo da página usamos um sleep de 10 segundos
        # para dar tempo de carregar todos os dados da página

        wait = WebDriverWait(driver, 5)

        link = wait.until(EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Registros de Vacinação COVID19')))
        link.click()

        link = wait.until(EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Dados SC')))
        href = link.get_attribute('href')

        driver.quit()

        url = href

        print("Fazendo download dos dados de Vacinação do MS...", end='', flush=True)

        os.system("wget -O dados_vacinacao.csv " + href)

        print(" Ok!")

        dir_atual = r"{}".format(os.getcwd() + '/back-end/dados_vacinacao.csv')
        # dir_atual = r"{}".format('/home/arthurssd/Documents/IFC/PROJETO DE PESQUISA/CÓDIGO/subcomite-cientifico/back-end/dados_head.csv')

        dir_MS = r"{}".format(
            os.getcwd() + '/back-end/Dados_MS/dados_vacinacao.csv')
        # dir_MS = r"{}".format('/home/arthurssd/Documents/IFC/PROJETO DE PESQUISA/CÓDIGO/subcomite-cientifico/back-end/Dados_MS/dados_head.csv')

        os.rename(dir_atual, dir_MS)

    def getFileLocal(self):

        dir_path = os.getcwd() + '/back-end/Dados_MS/dados_vacinacao.csv'
        # dir_path = '/home/arthurssd/Documents/IFC/PROJETO DE PESQUISA/CÓDIGO/subcomite-cientifico/back-end/Dados_MS/dados_vacinacao.csv'

        return dir_path

    def processaVacinacaoMS(self):

        tabelas = Tabelas()

        print("Processando dados de vacinação do MS...", end='', flush=True)

        # DADOS VACINADOS
        tabela = [2, 4, 5, 17, 20, 21, 27, 28, 29]

        {2: "paciente_idade", 4: "paciente_enumsexobiologico", 5: "paciente_racacor_codigo", 17: "estabelecimento_municipio_codigo",
            20: "vacina_grupoatendimento_codigo", 21: "vacina_grupoatendimento_nome", 27: "vacina_dataaplicacao", 28: "vacina_descricao_dose", 29: "vacina_codigo"}

        df = pd.read_csv(self.getFileLocal(),
                         usecols=tabela,
                         sep=";")

        # df['regional'] = [tabelas.getRegionalMunicipioBrasil(int(cod[0])) for cod in df['estabelecimento_municipio_codigo'].iteritems()]
        df.insert(1, 'regional', df['estabelecimento_municipio_codigo'])
        df['regional'] = df['regional'].replace(tabelas.municipios)

        df['doses_aplicadas'] = np.zeros(len(df))

        municipio_grupos_doses_dia = df.groupby(['regional', 'estabelecimento_municipio_codigo', 'vacina_grupoatendimento_codigo',
                                                'vacina_dataaplicacao', 'vacina_descricao_dose'], as_index=False)['doses_aplicadas'].count()

        #print("\n", municipio_grupos_doses_dia)

        print(" Ok!")

        self.salvaBD(municipio_grupos_doses_dia, self.param_dic)

    def connect(self):
        try:
            conn = psycopg2.connect(**self.param_dic)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)

        return conn

    def salvaBD(self, df, param_dic, table='vacinacao_ms'):

        df['data'] = pd.to_datetime(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        print("Salvando os dados... ", end='', flush=True)
        connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            self.param_dic['user'],
            quote(self.param_dic['password']),
            self.param_dic['host'],
            self.param_dic['database']
        )
        engine = create_engine(connect)
        df.to_sql(
            table,
            con=engine,
            index=False,
            # if_exists='append'
            if_exists='replace'
        )
        print(" Ok.")


# if __name__ == "__main__":
#     dowVacMS = download_vacinados_MS()
#     # dowVacMS.getFile()
#     dowVacMS.processaVacinacaoMS()
