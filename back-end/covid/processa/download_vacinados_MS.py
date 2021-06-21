import os
import time
import pandas as pd

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

        # O <endereço> de constar na seguinte linha de código webdrive.Chrome(..., executable_path='<endereço>')

        path_chromedriver = os.getcwd + '/chromedriver'

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

        # print(url)

        os.system("wget -O dados_vacinacao.csv " + href)

    def processaDataframe():

        df = pd.read_csv("dados_vacinacao.csv", sep=";")
        # print(df)

        remove_info = [
            'paciente_dataNascimento',
            'paciente_endereco_coPais',
            'paciente_endereco_nmMunicipio',
            'paciente_endereco_nmpais',
            'paciente_endereco_uf',
            'paciente_endereco_cep',
            'paciente_nacionalidade_enumnacionalidade',
            'estalecimento_nofantasia',
            'estabelecimento_uf',
            '',
            '',
            '',
            '',
            '',
            '',
            'id_sistema_origem',
        ]

        # "document_id";"paciente_id";"paciente_idade";"paciente_datanascimento";"paciente_enumsexobiologico";
# "paciente_racacor_codigo";"paciente_racacor_valor";"paciente_endereco_coibgemunicipio";"paciente_endereco_copais";
# "paciente_endereco_nmmunicipio";"paciente_endereco_nmpais";"paciente_endereco_uf";"paciente_endereco_cep";
# "paciente_nacionalidade_enumnacionalidade";"estabelecimento_valor";"estabelecimento_razaosocial";"estalecimento_nofantasia";
# "estabelecimento_municipio_codigo";"estabelecimento_municipio_nome";"estabelecimento_uf";"vacina_grupoatendimento_codigo";
# "vacina_grupoatendimento_nome";"vacina_categoria_codigo";"vacina_categoria_nome";"vacina_lote";"vacina_fabricante_nome";
# "vacina_fabricante_referencia";"vacina_dataaplicacao";"vacina_descricao_dose";"vacina_codigo";"vacina_nome";"sistema_origem";
# "data_importacao_rnds";"id_sistema_origem"

        df = df.drop(remove_info)

    def salvaBD():
        pass
