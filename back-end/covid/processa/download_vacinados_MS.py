from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from urllib.parse import quote
from sqlalchemy import create_engine
import os
import pandas as pd
import numpy as np
import psycopg2

from covid.processa.db.create import Create
from covid.processa.dados.tabelas import Tabelas

"""
A execução script precisa que o webdrive do Chrome seja instalado, para
que o Selenium possa simular a entrada no site.

Para isso é necessário instalar o webdrive apropriado para cada SO, ver em:
https://www.selenium.dev/documentation/en/selenium_installation/installing_webdriver_binaries/

"""


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--remote-debugging-port=9222")  # this


class download_vacinados_MS:

    def __init__(self):
        self.create = Create()

        self.grupos_prioritarios = {
            0:  "nan",
            101:  "Anemia Falciforme",
            102:  "Câncer",
            103:  "Diabetes Mellitus",
            104:  "Doença Pulmonar Obstrutiva Crônica",
            105:  "Doença Renal",
            106:  "Doenças Cardiovasculares e Cerebrovasculares",
            107:  "Hipertensão de difícil controle ou com complicações/lesão de órgão alvo",
            108:  "Indivíduos Transplantados de Órgão Sólido",
            109: "Obesidade Grave (Imc>=40)",
            110:  "Síndrome de Down",
            111:  "nan",
            112:  "Indivíduos Transplantados de Medula Óssea",
            114:  "nan",
            115:  "nan",
            116:  "nan",
            201: "Pessoas de 18 a 64 anos",
            202: "Pessoas de 65 a 69 anos",
            203: "Pessoas de 70 a 74 anos",
            204: "Pessoas de 75 a 79 anos",
            205: "Pessoas de 80 anos ou mais",
            301: "Pessoas de 60 nos ou mais Institucionalizadas",
            401:  "Marinha do Brasil - MB",
            402:  "Exército Brasileiro - EB",
            403:  "Força Aérea Brasileira - FAB",
            501:  "Bombeiro Civil",
            502:  "Bombeiro Militar",
            503:  "Guarda Municipal",
            504:  "Policial Rodoviário Federal",
            505:  "Policial Civil",
            506:  "Policial Federal",
            507:  "Policial Militar",
            601:  "Quilombola",
            602:  "Ribeirinha",
            701:  "Povos indígenas em terras indígenas",
            801:  "Ensino Básico",
            802:  "Ensino Superior",
            901:  "Auxiliar de Veterinário",
            902:  "Biólogo",
            903:  "Biomédico",
            904:  "Cozinheiro e Auxiliares",
            905:  "Cuidador de Idosos",
            906:  "Doula/Parteira",
            907:  "Enfermeiro(a)",
            908:  "Farmacêutico",
            909:  "Fisioterapeutas",
            910:  "Fonoaudiólogo",
            911:  "Funcionário do Sistema Funerário c/ cadáveres potencialmente contaminados",
            912:  "Médico",
            913:  "Médico Veterinário",
            914:  "Motorista de Ambulância",
            915:  "Nutricionista",
            916:  "Odontologista",
            917:  "Pessoal da Limpeza",
            918:  "Profissionais de Educação Física",
            919:  "Psicólogo",
            920:  "Recepcionista",
            921:  "Segurança",
            922:  "Assistente Social",
            923:  "Técnico de Enfermagem",
            924:  "Técnico de Veterinário",
            925:  "Terapeuta Ocupacional",
            926:  "Outros",
            927:  "Auxiliar de Enfermagem",
            928:  "Técnico de Odontologia",
            929:  "Estudante",
            930:  "nan",
            931:  "nan",
            932:  "nan",
            933:  "nan",
            1001:  "nan",
            1002:  "nan",
            1003:  "nan",
            1004:  "nan",
            1005:  "Metroviário",
            1006:  "nan",
            1101:  "Pessoas com Deficiência Institucionalizadas",
            1102:  "Pessoas com Deficiências Permanente Grave",
            1201:  "Pessoas em Situação de Rua",
            1301:  "Trabalhadores Portuários",
            1401:  "Funcionário do Sistema de Privação de Liberdade",
            1501:  "População Privada de Liberdade",
            1601:  "Trabalhadores Industriais",
            1701:  "Trabalhadores de limpeza urbana e manejo de resíduos sólidos",
            1801:  "nan",
            1901:  "nan",
            999999:  "Outros Grupos"
        }

        self.param_dic = {
            "host": "127.0.0.1",
            "database": "covid",
            "user": "postgres",
            "password": "!admpasswd@covid"
        }

        self.db = self.connect()

    def getFile(self):

        # DOWNLOAD DO ARQUIVO DE VACINAÇÃO DO MS

        try:
            # O <endereço> de constar na seguinte linha de código webdrive.Chrome(..., executable_path='<endereço>')
            path_chromedriver = os.getcwd() + '/back-end/covid/chromedriver/chromedriver'

            driver = webdriver.Chrome(
                options=chrome_options, executable_path=r"{}".format(path_chromedriver))

            # A linha abaixo é bem comum, mas não teve o efeito desejado neste problema
            # Acredito que em função de que a página carrega antes e ficam requisições assíncronas em execução.
            # Por isso vamos usar time.sleep mais pra frente
            # driver.implicitly_wait(20)
            # A seguir o site específico da terceira página (aba) do dashboard

            driver.get(
                "https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao")

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

            print("Fazendo download dos dados de Vacinação do MS...\n")
            # os.system("wget -O Dados_Vacinas/dados_vacinacao.csv " + href)
            os.system("curl " + href + " -o Dados_Vacinas/dados_vacinacao.csv")

            print("\n Ok!")

        except Exception as error:
            print("Error: ", error)
            print(r"Chrome path: {}".format(path_chromedriver))
            return None
        return 1

    def getFileLocal(self):

        dir_path = os.getcwd() + '/Dados_Vacinas/dados_vacinacao.csv'
        # dir_path = '/home/arthurssd/Documents/IFC/PROJETO DE PESQUISA/CÓDIGO/subcomite-cientifico/back-end/Dados_Vacinas/dados_vacinacao.csv'

        return dir_path

    def processaVacinacaoMS(self):

        tabelas = Tabelas()

        print("Processando dados de vacinação do MS...", end='', flush=True)

        # DADOS VACINADOS
        tabela = [2, 4, 5, 17, 20, 21, 27, 28, 29]

        try:
            df = pd.read_csv(self.getFileLocal(),
                             usecols=tabela,
                             sep=";")

            # preenche a nova tabela "regional" com o código IBGE do municipio respectivo
            df.insert(1, 'regional', df['estabelecimento_municipio_codigo'])

            # substitiu o código pela respectiva regional da saúde
            df['regional'] = df['regional'].replace(tabelas.municipios)

            # renomeia colunas
            df = df.rename(columns={'estabelecimento_municipio_codigo': 'municipio',
                                    'vacina_grupoatendimento_codigo': 'codigo_grupoatendimento'})

            # 3 comandos a seguir retiram os grupos de atendimento

            # dataframe = df[['vacina_grupoatendimento_nome',
            #                 'codigo_grupoatendimento']].drop_duplicates()
            # lista = list(dataframe[['vacina_grupoatendimento_nome',
            #                         'codigo_grupoatendimento']].values.tolist())
            # dictionary = {index[1]: index[0] for index in lista}

            # setar codigo grupo de atendimento como 0 em nome do grupo de atendimento nan
            # df.loc[df['vacina_grupoatendimento_nome'].isnull(),
            #        'codigo_grupoatendimento'] = 0

            # zera toda a coluna doses_aplicadas
            df['doses_aplicadas'] = np.zeros(len(df))

            # atribui a coluna dos munícipios como Int
            df['doses_aplicadas'] = df['doses_aplicadas'].astype(int)
            df['municipio'] = df['municipio'].astype(int)
            df['regional'] = df['regional'].astype(int)

            df['vacina_descricao_dose'] = df['vacina_descricao_dose'].str.strip()

            # agrupa dados com os mesmos valores para fazer a contagem de vacinados
            municipio_grupos_doses_dia = df.groupby(['regional', 'municipio',
                                                    'vacina_dataaplicacao', 'vacina_descricao_dose'], as_index=False)['doses_aplicadas'].count()

            # SE USAR GRUPO DE ATENDIMENTO, UM AJUSTE É PRECISO NA VIEW E NA TABELA
            # municipio_grupos_doses_dia = df.groupby(['codigo_grupoatendimento', 'regional', 'municipio',
            #                                         'vacina_dataaplicacao', 'vacina_descricao_dose'], as_index=False)['doses_aplicadas'].count()

            municipio_grupos_doses_dia['vacina_dataaplicacao'] = pd.to_datetime(
                municipio_grupos_doses_dia['vacina_dataaplicacao']).dt.date

            # USAR PARA QUANDO OS GRUPOS DE ATENDIMENTO FOREM USADOS
            # municipio_grupos_doses_dia['doses_aplicadas_sum'] = municipio_grupos_doses_dia.groupby(
            #     ['vacina_dataaplicacao', 'regional', 'municipio', 'vacina_descricao_dose'])['doses_aplicadas'].cumsum()

            # print(municipio_grupos_doses_dia)

            print(" Ok!")

        except Exception as error:
            print("Error: %s" % error)

        # print("\n", municipio_grupos_doses_dia)

        self.salvaBD(municipio_grupos_doses_dia, self.param_dic)
        self.create.create_view_vacinacao()

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
            datetime.now().strftime("%d/%m/%Y")).date()

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
