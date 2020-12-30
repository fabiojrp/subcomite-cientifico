
from Database import Database


class Create:

    def __init__(self):
        self.db = Database.get_instance()

    def create_table(self):
        print("Limpando e criando as tabelas...")
        # Limpa as tabelas
        self.db.execute_query("DROP TABLE IF EXISTS dados")
        self.db.execute_query("DROP TABLE IF EXISTS casos")
        

        sql = """
        DO $$
            BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'recuperado') THEN
                    CREATE TYPE recuperado AS ENUM('SIM','NAO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'internacao') THEN
                    CREATE  TYPE internacao AS ENUM('INTERNADO','NAO INTERNADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'internacao') THEN
                    CREATE  TYPE internacao AS ENUM('INTERNADO','NAO INTERNADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'internacao_uti') THEN
                CREATE TYPE internacao_uti AS ENUM('NAO INTERNADO UTI','INTERNADO UTI');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sexo') THEN
                CREATE TYPE sexo AS ENUM('FEMININO','MASCULINO','NAO INFORMADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'obito') THEN
                CREATE TYPE obito AS ENUM('SIM','NAO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'regional') THEN
                CREATE TYPE regional AS ENUM('FOZ DO RIO ITAJAI','SUL','GRANDE FLORIANOPOLIS','GRANDE OESTE','ALTO VALE DO ITAJAI','PLANALTO NORTE E NORDESTE','MEIO OESTE E SERRA CATARINENSE','OUTROS ESTADOS','OUTROS PAISES');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'raca') THEN
                CREATE TYPE raca AS ENUM('AMARELA','BRANCA','IGNORADO','INDIGENA','NAO INFORMADO','PARDA','PRETA');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado') THEN
                CREATE TYPE estado AS ENUM('SANTA CATARINA','NULL');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'criterio_confirmacao') THEN
                CREATE TYPE criterio_confirmacao AS ENUM('LABORATORIAL','CLINICO-EPIDEMIOLOGICO','IGNORADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'classificacao') THEN
                CREATE TYPE classificacao AS ENUM('CONFIRMADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_teste') THEN
                CREATE TYPE tipo_teste AS ENUM('IMUNOLOGICO (TESTE RAPIDO)','BIOLOGIA MOLECULAR (RT-PCR)','NAO SE APLICA','IGNORADO');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'reg_saude') THEN
                CREATE TYPE reg_saude AS ENUM('GRANDE FLORIANOPOLIS','MEDIO VALE DO ITAJAI','XANXERE','FOZ DO RIO ITAJAI','NORDESTE','ALTO VALE DO RIO DO PEIXE','SERRA CATARINENSE','MEIO OESTE','CARBONIFERA','ALTO URUGUAI CATARINENSE','OESTE','EXTREMO SUL CATARINENSE','EXTREMO OESTE','LAGUNA','ALTO VALE DO ITAJAI','PLANALTO NORTE','OUTROS ESTADOS','NULL');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sim_nao') THEN
                CREATE TYPE sim_nao AS ENUM('SIM','NAO');
            END IF;

            END
        $$;


            CREATE TABLE IF NOT EXISTS  dados (
                    data_publicacao timestamp NULL DEFAULT NULL,
                    recuperados recuperado DEFAULT 'SIM',
                    data_inicio_sintomas date DEFAULT NULL,
                    data_coleta date DEFAULT NULL,
                    sintomas varchar(512) DEFAULT NULL,
                    comorbidades varchar(512) DEFAULT NULL,
                    gestante varchar(64) DEFAULT NULL,
                    internacao internacao DEFAULT NULL,
                    internacao_uti internacao_uti DEFAULT NULL,
                    sexo sexo DEFAULT NULL,
                    municipio varchar(255) DEFAULT NULL,
                    obito obito DEFAULT NULL,
                    data_obito date DEFAULT NULL,
                    idade int DEFAULT NULL,
                    regional regional DEFAULT NULL,
                    raca raca DEFAULT NULL,
                    data_resultado timestamp NULL DEFAULT NULL,
                    codigo_ibge_municipio integer DEFAULT NULL,
                    latitude varchar(100) DEFAULT NULL,
                    longitude varchar(100) DEFAULT NULL,
                    estado estado DEFAULT NULL,
                    criterio_confirmacao criterio_confirmacao DEFAULT NULL,
                    tipo_teste tipo_teste DEFAULT NULL,
                    municipio_notificacao varchar(255) DEFAULT NULL,
                    codigo_ibge_municipio_notificacao integer DEFAULT NULL,
                    latitude_notificacao varchar(100) DEFAULT NULL,
                    longitude_notificacao varchar(100) DEFAULT NULL,
                    classificacao classificacao DEFAULT NULL,
                    origem_esus sim_nao DEFAULT NULL,
                    origem_sivep sim_nao DEFAULT NULL,
                    origem_lacen sim_nao DEFAULT NULL,
                    origem_laboratorio_privado sim_nao DEFAULT NULL,
                    nom_laboratorio varchar(100) DEFAULT NULL,
                    fez_teste_rapido sim_nao DEFAULT NULL,
                    fez_pcr sim_nao DEFAULT NULL,
                    data_internacao date DEFAULT NULL,
                    data_entrada_uti date DEFAULT NULL,
                    regional_saude reg_saude DEFAULT NULL,
                    data_evolucao_caso date DEFAULT NULL,
                    data_saida_uti date DEFAULT NULL,
                    bairro varchar(100) DEFAULT NULL
                )
"""

        self.db.execute_query(sql)

        sql = """CREATE TABLE IF NOT EXISTS casos (
                    codigo_ibge_municipio integer DEFAULT NULL,
                    populacao integer DEFAULT NULL,
                    regional integer DEFAULT NULL,
                    data date DEFAULT NULL,
                    casos integer DEFAULT NULL,
                    obitos integer DEFAULT NULL,
                    casos_acumulados integer DEFAULT NULL,
                    obitos_acumulados integer DEFAULT NULL,
                    casos_mediaMovel NUMERIC(10,5) DEFAULT NULL,
                    obitos_mediaMovel NUMERIC(10,5) DEFAULT NULL,
                    casos_acumulados_100mil NUMERIC(10,5) DEFAULT NULL,
                    obitos_acumulados_100mil NUMERIC(10,5) DEFAULT NULL,
                    casos_variacao_14dias NUMERIC(10,5) DEFAULT NULL,
                    obitos_variacao_14dias NUMERIC(10,5) DEFAULT NULL,
                    casos_diarios_100mil NUMERIC(10,5) DEFAULT NULL,
                    obitos_diarios_100mil NUMERIC(10,5) DEFAULT NULL,
                    letalidade_100_confirmados NUMERIC(10,5) DEFAULT NULL,
                    incidencia_100mil NUMERIC(10,5) DEFAULT NULL,
                    casos_ativos NUMERIC(10,5) DEFAULT NULL
                )
        """
        self.db.execute_query(sql)

        print("OK")


