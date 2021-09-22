from covid.processa.dao.Database import Database


class Create:
    def __init__(self):
        self.db = Database.get_instance()

    def create_rt(self):
        print("Criando as tabelas de rt...", end='', flush=True)

        self.db.execute_query("""CREATE TABLE IF NOT EXISTS rt_municipio(
                                    regional integer,
                                    codigo_ibge_municipio integer,
                                    data date,
                                    valor_r NUMERIC(17,2) DEFAULT NULL::numeric)
                            """)

        self.db.execute_query("""CREATE TABLE IF NOT EXISTS rt_regional(
                                    regional integer,
                                    data date,
                                    valor_r NUMERIC(17,2) DEFAULT NULL::numeric
                                )
                            """)

        print("OK")

    def create_leitos(self):
        print("Limpando e criando as tabelas de leitos...", end='', flush=True)

        # Limpa as tabelas

        sql = """CREATE TABLE IF NOT EXISTS leitosGeraisCovid (
                    macrorregiao varchar(100) DEFAULT NULL,
                    hospital varchar(100) DEFAULT NULL,
                    municipio varchar(100) DEFAULT NULL,
                    codigo_ibge_municipio integer DEFAULT NULL,
                    regional_saude varchar(100) DEFAULT NULL,
                    index_regional integer DEFAULT NULL,
                    leitos_ativos integer DEFAULT NULL,
                    leitos_ocupados integer DEFAULT NULL,
                    leitos_disponiveis integer DEFAULT NULL,
                    taxa_ocupacao NUMERIC(5,2) DEFAULT NULL,
                    pacientes_covid integer DEFAULT NULL,
                    atualizacao timestamp DEFAULT NULL
                )
        """
        self.db.execute_query(sql)

        sql = """CREATE TABLE IF NOT EXISTS leitosCovid (
                    macrorregiao varchar(100) DEFAULT NULL,
                    hospital varchar(100) DEFAULT NULL,
                    municipio varchar(100) DEFAULT NULL,
                    codigo_ibge_municipio integer DEFAULT NULL,
                    regional_saude varchar(100) DEFAULT NULL,
                    index_regional integer DEFAULT NULL,
                    leitos_ativos integer DEFAULT NULL,
                    leitos_ocupados integer DEFAULT NULL,
                    leitos_disponiveis integer DEFAULT NULL,
                    taxa_ocupacao NUMERIC(5,2) DEFAULT NULL,
                    pacientes_covid integer DEFAULT NULL,
                    atualizacao timestamp DEFAULT NULL
                )
        """
        self.db.execute_query(sql)

        print("OK")

    def create_table_brasil(self):
        print("Limpando e criando as tabelas...")
        # Apagando as views
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_CASOS_ANTERIOR")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_CASOS_ATUAL")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOS")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_RT")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_INCIDENCIA")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_VACINACAO")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_DADOS_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOS_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOS_MAX")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOS_COVID_MAX")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_RT_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_VACINACAO_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_INCIDENCIA_LETALIDADE_REG_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_INCIDENCIA_LETALIDADE_SC_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_VARIACAO_MM_BOLETIM")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_VACINACAO_MS CASCADE")
           
        # Limpa as tabelas
        self.db.execute_query("DROP TABLE IF EXISTS CASOSBRASIL")
        self.db.execute_query("DROP TABLE IF EXISTS casos")
        self.db.execute_query("DROP TABLE IF EXISTS vacinacao_ms CASCADE")

        sql = """
            CREATE TABLE IF NOT EXISTS CASOSBRASIL(
                REGIAO VARCHAR(32) DEFAULT NULL,
                ESTADO VARCHAR(8) DEFAULT NULL,
                MUNICIPIO VARCHAR(256) DEFAULT NULL,
                CODUF int DEFAULT NULL,
                CODMUN int DEFAULT NULL,
                CODREGIAOSAUDE int DEFAULT NULL,
                NOMEREGIAOSAUDE VARCHAR(256) DEFAULT NULL,
                DATA date DEFAULT NULL,
                SEMANAEPI int DEFAULT NULL,
                POPULACAOTCU2019 int DEFAULT NULL,
                CASOSACUMULADO int DEFAULT NULL,
                CASOSNOVOS int DEFAULT NULL,
                OBITOSACUMULADO int DEFAULT NULL,
                OBITOSNOVOS int DEFAULT NULL,
                RECUPERADOSNOVOS int DEFAULT NULL,
                EMACOMPANHAMENTONOVOS int DEFAULT NULL,
                INTERIOR_METROPOLITANA int DEFAULT NULL
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
                    casos_mediaMovel NUMERIC(17,5) DEFAULT NULL,
                    obitos_mediaMovel NUMERIC(17,5) DEFAULT NULL,
                    variacao_mediaMovel_casos NUMERIC(17,5) DEFAULT NULL,
                    casos_acumulados_100mil NUMERIC(22,6) DEFAULT NULL,
                    obitos_acumulados_100mil NUMERIC(26,6) DEFAULT NULL,
                    casos_variacao_14dias NUMERIC(17,5) DEFAULT NULL,
                    obitos_variacao_14dias NUMERIC(17,5) DEFAULT NULL,
                    incidencia_casos_diarios_100mil NUMERIC(17,5) DEFAULT NULL,
                    incidencia_obitos_diarios_100mil NUMERIC(17,5) DEFAULT NULL,
                    letalidade_100_confirmados NUMERIC(17,5) DEFAULT NULL,
                    casos_ativos integer DEFAULT NULL
                )
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_rt AS SELECT REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID,
                    REGIONAIS.POLIGONO::JSONB,
                    REGIONAIS.URL AS URL,
                    RT_REGIONAL.DATA AS DATA,
                    RT_REGIONAL.VALOR_R AS RT
                FROM REGIONAIS, RT_REGIONAL
                WHERE RT_REGIONAL.DATA = (SELECT MAX(RT_REGIONAL.DATA) FROM RT_REGIONAL)
                                AND RT_REGIONAL.REGIONAL = REGIONAIS.ID
                ORDER BY REGIONAIS.REGIONAL_SAUDE,
                    RT_REGIONAL.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_casos_atual AS SELECT REGIONAIS.ID,
                    CASOS.DATA,
                    SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                FROM REGIONAIS,
                    CASOS
                WHERE CASOS.DATA = (SELECT MAX(CASOS.DATA) - interval '1 day' AS MAX_DATA FROM CASOS)
                                AND CASOS.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID,
                    CASOS.DATA
                ORDER BY CASOS.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_casos_anterior AS SELECT REGIONAIS.ID,
                    CASOS.DATA,
                    SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                FROM REGIONAIS,
                    CASOS
                WHERE CASOS.DATA = (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS) - interval '14 day'
                                AND CASOS.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID,
                    CASOS.DATA
                ORDER BY CASOS.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_leitos AS SELECT REGIONAIS.ID,
                    SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                    SUM(leitoscovid.leitos_ocupados) AS LEITOS_OCUPADOS,
                    MAX(leitoscovid.ATUALIZACAO) AS MAX_DATA
                FROM REGIONAIS, leitoscovid
                WHERE leitoscovid.ATUALIZACAO =
                    (SELECT MAX(leitoscovid.ATUALIZACAO) AS MAX_DATA FROM leitoscovid)
                    AND leitoscovid.INDEX_REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_incidencia AS SELECT REGIONAIS.ID,
                    CASOS.DATA,
                    CASE WHEN (SUM(CASOS.CASOS_ACUMULADOS) < 100) THEN 0
                                    ELSE (SUM(CASOS.OBITOS_ACUMULADOS)::real / SUM(CASOS.CASOS_ACUMULADOS)::real) * 100
                    END AS LETALIDADE,
                    CASE WHEN (SUM(CASOS.POPULACAO) <= 0) THEN 0
                                    ELSE (SUM(CASOS.CASOS_ACUMULADOS)::real / SUM(CASOS.POPULACAO)::real) * 1e5
                    END AS INCIDENCIA
                FROM REGIONAIS,
                    CASOS
                WHERE CASOS.REGIONAL = REGIONAIS.ID
                                AND CASOS.DATA = (SELECT MAX(CASOS.DATA) FROM CASOS)
                GROUP BY REGIONAIS.ID,
                    CASOS.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_vacinacao AS 
                SELECT REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID AS ID,
                    REGIONAIS.POPULACAO AS POPULACAO,
                    SUM(VACINACAO_DIVE."D1") AS VACINACAO_D1,
                    SUM(VACINACAO_DIVE."D2") AS VACINACAO_D2,
                    VACINACAO_DIVE."Data" AS DATA
                FROM REGIONAIS,
                    VACINACAO_DIVE
                WHERE VACINACAO_DIVE."Data" = (SELECT MAX(VACINACAO_DIVE."Data") AS MAX_DATA FROM VACINACAO_DIVE)
                    AND VACINACAO_DIVE.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID,
                    REGIONAIS.REGIONAL_SAUDE, 
                    VACINACAO_DIVE."Data"
                ORDER BY REGIONAIS.ID
        """
        self.db.execute_query(sql)

        sql = """CREATE OR REPLACE VIEW VIEW_LEITOS_MAX AS
                SELECT REGIONAIS.REGIONAL_SAUDE,
                    TBL.ID,
                    TBL.LEITOS_OCUPADOS,
                    TBL.LEITOS_ATIVOS,
					MAX(TBL.LEITOS_ATIVOS) OVER (PARTITION BY TBL.ID  ORDER BY DATA) AS LEITOS_ATIVOS_MAX,
                    TBL.DATA AS DATA
                FROM
                    (SELECT LEITOSGERAISCOVID.INDEX_REGIONAL AS ID,
                            SUM(LEITOSGERAISCOVID.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                            SUM(LEITOSGERAISCOVID.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                            (LEITOSGERAISCOVID.ATUALIZACAO) AS DATA
                        FROM LEITOSGERAISCOVID
                        GROUP BY LEITOSGERAISCOVID.INDEX_REGIONAL,
                            LEITOSGERAISCOVID.ATUALIZACAO
                        ORDER BY LEITOSGERAISCOVID.INDEX_REGIONAL,
                            LEITOSGERAISCOVID.ATUALIZACAO) AS TBL,
                    REGIONAIS
                WHERE TBL.ID = REGIONAIS.ID
                    AND TBL.DATA > '2021-06-11'
                ORDER BY TBL.ID,
                    TBL.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE OR REPLACE VIEW VIEW_LEITOS_COVID_MAX AS
                    SELECT REGIONAIS.REGIONAL_SAUDE,
                        TBL.ID,
                        TBL.LEITOS_OCUPADOS,
                        TBL.LEITOS_ATIVOS,
                        MAX(TBL.LEITOS_ATIVOS) OVER (PARTITION BY TBL.ID ORDER BY TBL.DATA) AS LEITOS_ATIVOS_MAX,
                        TBL.DATA
                    FROM
                        (SELECT LEITOSCOVID.INDEX_REGIONAL AS ID,
                                SUM(LEITOSCOVID.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                                SUM(LEITOSCOVID.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                                LEITOSCOVID.ATUALIZACAO AS DATA
                            FROM LEITOSCOVID
                            GROUP BY LEITOSCOVID.INDEX_REGIONAL,
                                LEITOSCOVID.ATUALIZACAO
                            ORDER BY LEITOSCOVID.INDEX_REGIONAL,
                                LEITOSCOVID.ATUALIZACAO) TBL,
                        REGIONAIS
                    WHERE TBL.ID = REGIONAIS.ID
                    ORDER BY TBL.ID,
                        TBL.DATA;
        """
        self.db.execute_query(sql)
        
        # RT boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_RT_BOLETIM AS
        SELECT 
            REGIONAIS.REGIONAL_SAUDE,
            REGIONAIS.ID,
            RT_REGIONAL.DATA,
            RT_REGIONAL.VALOR_R AS RT
        FROM REGIONAIS, RT_REGIONAL
        WHERE RT_REGIONAL.DATA >= '2021-07-21'
            AND RT_REGIONAL.REGIONAL = REGIONAIS.ID
        AND REGIONAIS.ID <> 1
        ORDER BY REGIONAIS.ID,
            RT_REGIONAL.DATA
        """
        self.db.execute_query(sql)
        
        # leitos boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_LEITOS_BOLETIM AS
        SELECT
            VIEW_LEITOS_MAX.ID,
            VIEW_LEITOS_MAX.REGIONAL_SAUDE,
            VIEW_LEITOS_MAX.LEITOS_OCUPADOS,
            VIEW_LEITOS_MAX.LEITOS_ATIVOS,
            VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX,
            VIEW_LEITOS_MAX.DATA::DATE
        FROM VIEW_LEITOS_MAX
            WHERE VIEW_LEITOS_MAX.DATA >= '2021-07-21'
        ORDER BY VIEW_LEITOS_MAX.ID,
            VIEW_LEITOS_MAX.DATA
        """
        self.db.execute_query(sql)
        
        # variacao boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_VARIACAO_MM_BOLETIM AS
        SELECT 
            REGIONAIS.ID,
            CASOS_ATUAL.DATA,
            ((CASOS_ATUAL.CASOS_MEDIAMOVEL::NUMERIC / CASOS_ANTERIOR.CASOS_MEDIAMOVEL::NUMERIC - 1) * 100) AS VARIACAO_MM
        FROM REGIONAIS,
            (SELECT 
                REGIONAIS.ID,
                CASOS.DATA,
                SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
            FROM REGIONAIS,CASOS
            WHERE CASOS.DATA >= '2021-07-21'::DATE - INTERVAL '14 DAYS'
                AND CASOS.DATA < (SELECT MAX(DATA)::DATE - INTERVAL '13 DAY' FROM CASOS)
                AND CASOS.REGIONAL = REGIONAIS.ID
                AND CASOS.REGIONAL <> 0
                AND CASOS.REGIONAL <> 1
            GROUP BY REGIONAIS.ID, CASOS.DATA
            ORDER BY REGIONAIS.ID, CASOS.DATA
            ) AS CASOS_ANTERIOR,
            
            (SELECT 
                REGIONAIS.ID,
                CASOS.DATA,
                SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
            FROM REGIONAIS, CASOS
            WHERE CASOS.DATA >= '2021-07-21' 
                AND CASOS.REGIONAL = REGIONAIS.ID
                AND CASOS.REGIONAL <> 0
                AND CASOS.REGIONAL <> 1
            GROUP BY REGIONAIS.ID, CASOS.DATA
            ORDER BY REGIONAIS.ID, CASOS.DATA 
            ) AS CASOS_ATUAL
        WHERE CASOS_ATUAL.ID = CASOS_ANTERIOR.ID
            AND CASOS_ATUAL.ID = REGIONAIS.ID
            AND CASOS_ANTERIOR.DATA = CASOS_ATUAL.DATA::DATE - INTERVAL '14 days'
        """
        self.db.execute_query(sql)
        
        # letalidade e incidencia regionais boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_INCIDENCIA_LETALIDADE_REG_BOLETIM AS
        SELECT 
            REGIONAIS.ID,
            CASOS.DATA,
            CASE WHEN (SUM(CASOS.CASOS_ACUMULADOS) < 100) THEN 0 ELSE (SUM(CASOS.OBITOS_ACUMULADOS)::real / SUM(CASOS.CASOS_ACUMULADOS)::real) * 100
            END AS LETALIDADE,
            CASE WHEN (SUM(CASOS.POPULACAO) <= 0) THEN 0 ELSE (SUM(CASOS.CASOS_ACUMULADOS)::real / SUM(CASOS.POPULACAO)::real) * 1e5
            END AS INCIDENCIA
        FROM REGIONAIS, CASOS
        WHERE CASOS.REGIONAL = REGIONAIS.ID
            AND CASOS.DATA >= '2021-07-21'
        GROUP BY CASOS.DATA, REGIONAIS.ID
        """
        self.db.execute_query(sql)
        
        # letalidade e incidencia estado boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_INCIDENCIA_LETALIDADE_SC_BOLETIM AS
        SELECT 
            REGIONAIS.ID,
            CASOS.DATA,
            CASE WHEN (SUM(CASOS.CASOS_ACUMULADOS) < 100) THEN 0 ELSE (SUM(CASOS.OBITOS_ACUMULADOS)::real / SUM(CASOS.CASOS_ACUMULADOS)::real) * 100
            END AS LETALIDADE,
            CASE WHEN (SUM(CASOS.POPULACAO) <= 0) THEN 0 ELSE (SUM(CASOS.CASOS_ACUMULADOS)::real / SUM(CASOS.POPULACAO)::real) * 1e5
            END AS INCIDENCIA
        FROM REGIONAIS, CASOS
        WHERE CASOS.REGIONAL = 1
            AND CASOS.REGIONAL = REGIONAIS.ID
            AND CASOS.DATA >= '2021-07-21'
        GROUP BY CASOS.DATA, REGIONAIS.ID
        """
        self.db.execute_query(sql)
        
        # vacinação boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_VACINACAO_BOLETIM AS
        SELECT 
            REGIONAIS.REGIONAL_SAUDE,
            REGIONAIS.ID AS ID,
            REGIONAIS.POPULACAO AS POPULACAO,
            SUM(VACINACAO_DIVE."D1") AS VACINACAO_D1,
            SUM(VACINACAO_DIVE."D2") AS VACINACAO_D2,
            VACINACAO_DIVE."Data" AS DATA
        FROM REGIONAIS,
            VACINACAO_DIVE
        WHERE VACINACAO_DIVE."Data" >= '2021-07-21'
            AND VACINACAO_DIVE.REGIONAL = REGIONAIS.ID
        GROUP BY VACINACAO_DIVE."Data", REGIONAIS.ID
        ORDER BY REGIONAIS.ID, VACINACAO_DIVE."Data"
        """
        self.db.execute_query(sql)
        
        # dados boletim
        sql = """ CREATE OR REPLACE VIEW VIEW_DADOS_BOLETIM AS
        SELECT 
            RT_REGIONAIS.ID,
            RT_REGIONAIS.REGIONAL_SAUDE,
            RT_REGIONAIS.DATA,
            RT_REGIONAIS.RT,
            TABELA_REGIONAIS.LETALIDADE,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            TABELA_REGIONAIS.INCIDENCIA,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            ((VACINACAO.VACINACAO_D2::REAL / VACINACAO.POPULACAO) * 100) AS D2_PERCENTUAL,
            (LEITOS_REGIONAIS.LEITOS_OCUPADOS::NUMERIC / LEITOS_REGIONAIS.LEITOS_ATIVOS::NUMERIC * 100) AS OCUPACAO_LEITOS,
            VARIACAO_REGIONAIS.VARIACAO_MM AS VARIACAO
        FROM
            VIEW_RT_BOLETIM AS RT_REGIONAIS,
            VIEW_LEITOS_BOLETIM AS LEITOS_REGIONAIS,
            VIEW_VARIACAO_MM_BOLETIM AS VARIACAO_REGIONAIS,
            VIEW_INCIDENCIA_LETALIDADE_REG_BOLETIM AS TABELA_REGIONAIS,
            VIEW_INCIDENCIA_LETALIDADE_SC_BOLETIM AS TABELA_ESTADO,
            VIEW_VACINACAO_BOLETIM AS VACINACAO
        WHERE RT_REGIONAIS.ID = VARIACAO_REGIONAIS.ID
            AND RT_REGIONAIS.DATA = VARIACAO_REGIONAIS.DATA
            AND RT_REGIONAIS.ID = TABELA_REGIONAIS.ID
            AND RT_REGIONAIS.DATA = TABELA_REGIONAIS.DATA
            AND RT_REGIONAIS.DATA = TABELA_ESTADO.DATA
            AND RT_REGIONAIS.ID = VACINACAO.ID
            AND RT_REGIONAIS.DATA = VACINACAO.DATA
            AND RT_REGIONAIS.ID = LEITOS_REGIONAIS.ID
            AND RT_REGIONAIS.DATA = LEITOS_REGIONAIS.DATA
            AND EXTRACT(DOW FROM RT_REGIONAIS.DATA) = 3
		ORDER BY RT_REGIONAIS.ID, RT_REGIONAIS.DATA
        """
        self.db.execute_query(sql)
        
        print("OK")

    def create_view_vacinacao(self):

        sql = """CREATE OR REPLACE VIEW view_vacinacao_ms AS
                SELECT REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID AS ID,
                    REGIONAIS.POPULACAO AS POPULACAO,
                    VACINACAO_MS.VACINA_DESCRICAO_DOSE AS VACINA_DESCRICAO_DOSE,
                    SUM(VACINACAO_MS.DOSES_APLICADAS) AS DOSES_APLICADAS,
                    VACINACAO_MS.DATA AS DATA
                FROM REGIONAIS,
                    VACINACAO_MS
                WHERE VACINACAO_MS.DATA = (SELECT MAX(VACINACAO_MS.DATA) AS MAX_DATA FROM VACINACAO_MS)
                    AND VACINACAO_MS.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID,
                    REGIONAIS.REGIONAL_SAUDE,
                    VACINACAO_MS.DATA,
                    VACINACAO_MS.VACINA_DESCRICAO_DOSE
                ORDER BY REGIONAIS.ID
        """
        self.db.execute_query(sql)

        sql = """CREATE OR REPLACE VIEW VIEW_VACINACAO_MS_POR_REGIAO AS
                SELECT TBL.REGIONAL_ID AS ID,
                        REGIONAIS.REGIONAL_SAUDE AS REGIONAL_SAUDE,
                        REGIONAIS.POPULACAO AS POPULACAO,
                        TBL.VACINA_DATAAPLICACAO AS DATA,
                        SUM(TBL.D1) OVER (PARTITION BY REGIONAL_ID ORDER BY REGIONAL_ID, VACINA_DATAAPLICACAO) AS D1,
                        SUM(TBL.D2) OVER (PARTITION BY REGIONAL_ID ORDER BY REGIONAL_ID, VACINA_DATAAPLICACAO) AS D2
                    FROM
                        (SELECT VACINACAO_MS.REGIONAL AS REGIONAL_ID,
                                DATE(VACINACAO_MS.VACINA_DATAAPLICACAO) AS VACINA_DATAAPLICACAO,
                                SUM(CASE WHEN VACINACAO_MS.VACINA_DESCRICAO_DOSE = '1ª Dose' THEN VACINACAO_MS.DOSES_APLICADAS END) AS D1,
                                SUM(CASE WHEN VACINACAO_MS.VACINA_DESCRICAO_DOSE IN ('2ª Dose', 'Única', 'Dose') THEN VACINACAO_MS.DOSES_APLICADAS END) AS D2
                            FROM VACINACAO_MS
                            GROUP BY VACINACAO_MS.REGIONAL,
                                VACINACAO_MS.VACINA_DATAAPLICACAO
                            ORDER BY VACINACAO_MS.REGIONAL ASC, DATE(VACINACAO_MS.VACINA_DATAAPLICACAO) ASC) AS TBL,
                        REGIONAIS
                    WHERE TBL.REGIONAL_ID = REGIONAIS.ID
        """
        self.db.execute_query(sql)

        sql = """CREATE OR REPLACE VIEW PUBLIC.VIEW_VACINACAO_MS_RESUMO AS
                    SELECT VACINACAO_MS.REGIONAL as ID,
                        SUM(VACINACAO_MS.DOSES_APLICADAS) AS DOSES_APLICADAS,
                        VACINACAO_MS.DATA
                    FROM VACINACAO_MS
                    WHERE VACINACAO_MS.DATA =
                            (SELECT MAX(VACINACAO_MS.DATA) AS MAX_DATA
                                FROM VACINACAO_MS)
                        AND VACINACAO_MS.VACINA_DESCRICAO_DOSE IN ('2ª Dose','Dose','Única')
                    GROUP BY VACINACAO_MS.REGIONAL,
                        VACINACAO_MS.DATA
                    ORDER BY VACINACAO_MS.REGIONAL
        """
        self.db.execute_query(sql)

    def create_table(self):
        print("Limpando e criando as tabelas...")
        # Limpa as tabelas

        # Apagando as views
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_CASOS_ANTERIOR")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_CASOS_ATUAL")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_RT")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOS")
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_LEITOSGERAL")

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
                    incidencia_casos_diarios_100mil NUMERIC(10,5) DEFAULT NULL,
                    incidencia_obitos_diarios_100mil NUMERIC(10,5) DEFAULT NULL,
                    letalidade_100_confirmados NUMERIC(10,5) DEFAULT NULL,
                    casos_ativos integer DEFAULT NULL
                )
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_rt AS SELECT REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID,
                    REGIONAIS.POLIGONO::JSONB,
                    REGIONAIS.URL AS URL,
                    RT.DATA AS DATA,
                    RT.RT AS RT
                FROM REGIONAIS, RT
                WHERE RT.DATA = (SELECT MAX(RT.DATA) FROM RT)
                                AND RT.REGIONAL = REGIONAIS.ID
                ORDER BY REGIONAIS.REGIONAL_SAUDE,
                    RT.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_casos_atual AS SELECT REGIONAIS.ID,
                    CASOS.DATA,
                    SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                FROM REGIONAIS,
                    CASOS
                WHERE CASOS.DATA = (SELECT MAX(CASOS.DATA) - interval '1 day' AS MAX_DATA FROM CASOS)
                                AND CASOS.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID,
                    CASOS.DATA
                ORDER BY CASOS.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_casos_anterior AS SELECT REGIONAIS.ID,
                    CASOS.DATA,
                    SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                FROM REGIONAIS,
                    CASOS
                WHERE CASOS.DATA = (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS) - interval '14 day'
                                AND CASOS.REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID,
                    CASOS.DATA
                ORDER BY CASOS.DATA
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_leitos AS SELECT REGIONAIS.ID,
                    SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                    SUM(leitoscovid.leitos_ocupados) AS LEITOS_OCUPADOS,
                    MAX(leitoscovid.ATUALIZACAO) AS MAX_DATA
                FROM REGIONAIS, leitoscovid
                WHERE leitoscovid.ATUALIZACAO =
                    (SELECT MAX(leitoscovid.ATUALIZACAO) AS MAX_DATA FROM leitoscovid)
                    AND leitoscovid.INDEX_REGIONAL = REGIONAIS.ID
                GROUP BY REGIONAIS.ID
        """
        self.db.execute_query(sql)
        

        sql = """CREATE VIEW VIEW_LEITOSGERAL AS
                    SELECT REGIONAIS.REGIONAL_SAUDE,
                        SUM(LEITOSGERAISCOVID.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                        SUM(LEITOSGERAISCOVID.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                        MAX(LEITOSGERAISCOVID.ATUALIZACAO) AS MAX_DATA
                    FROM REGIONAIS,
                        LEITOSGERAISCOVID
                    WHERE LEITOSGERAISCOVID.ATUALIZACAO =
                            (SELECT MAX(LEITOSGERAISCOVID.ATUALIZACAO) AS MAX_DATA
                                FROM LEITOSGERAISCOVID)
                        AND LEITOSGERAISCOVID.INDEX_REGIONAL = REGIONAIS.ID
                    GROUP BY REGIONAIS.REGIONAL_SAUDE
        """
        self.db.execute_query(sql)

        print("OK")
