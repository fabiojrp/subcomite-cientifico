import sys
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import psycopg2


class daoIndicadores:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "port": 5432,
            "dbname": "covid",
            "user": "postgres",
            "password": "xxxx"
        }

    def __get_connection(self):
        try:
            conn = psycopg2.connect(**self.config)
            return conn
        except:
            print('Não é possível estabelecar conexão com o banco de dados.')
            sys.exit(1)


    def __get_engine(self):
        my_config = {}
        my_config['drivername'] = "postgresql"
        my_config['username'] = self.config['user']
        my_config['password'] = self.config['password']
        my_config['port'] = str(self.config['port'])
        my_config['host'] = str(self.config['host'])
        my_config['database'] = str(self.config['dbname'])
        url = URL(**my_config)
        return create_engine(url)


    def __consultar(self, sql, index = None):
        conn = self.__get_connection()
        data = pd.read_sql_query(sql, conn, index_col = index)
        return data

    def salvaBD(self, df, table='avaliacaoRegionais', type = 'append'):
        df['data_calculo'] = pd.to_datetime(
            datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        print("Salvando os dados... ", end='', flush=True)
        engine = self.__get_engine()
        df.to_sql(
            table,
            con=engine,
            index=True,
            if_exists=type
        )
        print(" Ok!")

    def salvaBDDiario(self, df, table='avaliacaoRegionaisDiario'):
        from sqlalchemy import dialects

        df['data_calculo'] = pd.to_datetime(
            datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        print("Salvando os dados... ", end='', flush=True)
        engine = self.__get_engine()
        df.to_sql(
            table,
            con=engine,
            index=True,
            if_exists='replace',
            dtype={"poligono":dialects.postgresql.JSONB}
        )
        print(" Ok!")

    def buscar_dados_atuais(self):
        sql = '''
        SELECT VIEW_RT.ID AS ID,
            VIEW_RT.REGIONAL_SAUDE AS REGIONAL,
            VIEW_RT.DATA,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VAR_MEDIA_MOVEL,
            VIEW_RT.RT AS RT,
            VIEW_INCIDENCIA.LETALIDADE,
            VIEW_INCIDENCIA.INCIDENCIA,
         	(VIEW_LEITOS_COVID_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_COVID_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_COVID_MAX, 
		 	(VIEW_LEITOS_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_GERAL_MAX,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            VIEW_VACINACAO.VACINACAO_D2 / VIEW_VACINACAO.POPULACAO AS VACINACAO_D2_DIVE,
            VIEW_VACINACAO_MS_RESUMO.DOSES_APLICADAS / VIEW_VACINACAO.POPULACAO AS VACINACAO_D2_MS
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS_COVID_MAX,
            VIEW_LEITOS_MAX,
            VIEW_INCIDENCIA,
            VIEW_VACINACAO,
            VIEW_VACINACAO_MS_RESUMO,
            (SELECT VIEW_INCIDENCIA.LETALIDADE,
                    VIEW_INCIDENCIA.INCIDENCIA
                FROM VIEW_INCIDENCIA
                WHERE VIEW_INCIDENCIA.ID = 1) AS TABELA_ESTADO
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
            AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
            AND VIEW_RT.ID = VIEW_LEITOS_MAX.ID
            AND VIEW_RT.ID = VIEW_LEITOS_COVID_MAX.ID
            AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
            AND VIEW_RT.ID = VIEW_VACINACAO.ID
            AND VIEW_RT.ID = VIEW_VACINACAO_MS_RESUMO.ID
            AND VIEW_LEITOS_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_MAX)
			AND VIEW_LEITOS_COVID_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_COVID_MAX)
        '''
        return self.__consultar(sql, ['id'])

    def buscar_dados_atuais_diario(self):
        sql = '''
        SELECT VIEW_RT.ID AS ID,
            VIEW_RT.REGIONAL_SAUDE AS REGIONAL,
			VIEW_RT.DATA AS DATA,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VAR_MEDIA_MOVEL,
            VIEW_RT.RT,
            VIEW_RT.poligono AS POLIGONO,
            VIEW_RT.url AS url,
         	(VIEW_LEITOS_COVID_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_COVID_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_COVID_MAX, 
		 	(VIEW_LEITOS_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_GERAL_MAX,
            VIEW_INCIDENCIA.INCIDENCIA,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            VIEW_INCIDENCIA.LETALIDADE,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            VIEW_VACINACAO.VACINACAO_D2 / VIEW_VACINACAO.POPULACAO AS VACINACAO_D2_DIVE,
            VIEW_VACINACAO_MS_RESUMO.DOSES_APLICADAS / VIEW_VACINACAO.POPULACAO AS VACINACAO_D2_MS
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS_MAX,
			VIEW_LEITOS_COVID_MAX,
            VIEW_INCIDENCIA,
            view_vacinacao,
            VIEW_VACINACAO_MS_RESUMO,
            (SELECT VIEW_INCIDENCIA.LETALIDADE, VIEW_INCIDENCIA.INCIDENCIA
                FROM VIEW_INCIDENCIA
                WHERE VIEW_INCIDENCIA.ID  = 1) as TABELA_ESTADO
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
            AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
            AND VIEW_RT.ID = VIEW_LEITOS_MAX.ID
            AND VIEW_RT.ID = VIEW_LEITOS_COVID_MAX.ID
            AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
            AND VIEW_RT.ID = VIEW_VACINACAO.ID
            AND VIEW_RT.ID = VIEW_VACINACAO_MS_RESUMO.ID
            AND VIEW_LEITOS_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_MAX)
			AND VIEW_LEITOS_COVID_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_COVID_MAX)
        '''
        return self.__consultar(sql, ['id'])

    def buscar_dados_atuais_sc_diario(self):
        sql = '''
        SELECT
            RT_REGIONAL.REGIONAL as ID,
            'Estado de Santa Catarina' as REGIONAL,
            RT_REGIONAL.DATA AS DATA, 
            RT_REGIONAL.VALOR_R AS RT,
            (CASOS_ATUAL.CASOS_MEDIAMOVEL / CASOS_ANTERIOR.CASOS_MEDIAMOVEL - 1) AS VAR_MEDIA_MOVEL,
            VIEW_INCIDENCIA.INCIDENCIA AS INCIDENCIA,
            VIEW_INCIDENCIA.LETALIDADE AS LETALIDADE,
            VIEW_INCIDENCIA.INCIDENCIA AS INCIDENCIA_SC,
            VIEW_INCIDENCIA.LETALIDADE AS LETALIDADE_SC,
            (VACINACAO_MS.D2_APLICADAS / CASOS.POPULACAO) AS VACINACAO_D2_MS,
            (VACINACAO_DIVE.D2_APLICADAS / CASOS.POPULACAO) AS VACINACAO_D2_DIVE,
            (LEITOS_COVID.LEITOS_OCUPADOS::NUMERIC / LEITOS_COVID.LEITOS_ATIVOS::NUMERIC) AS LEITOS_COVID_MAX,
            (LEITOS_GERAL.LEITOS_OCUPADOS::NUMERIC / LEITOS_GERAL.LEITOS_ATIVOS::NUMERIC) AS LEITOS_GERAL_MAX
        FROM RT_REGIONAL,
            VIEW_INCIDENCIA, CASOS,
            VIEW_CASOS_ANTERIOR AS CASOS_ANTERIOR,
            VIEW_CASOS_ATUAL AS CASOS_ATUAL,
            (SELECT SUM(DOSES_APLICADAS) AS D2_APLICADAS FROM view_vacinacao_ms  WHERE VACINA_DESCRICAO_DOSE IN ('2ª Dose', '2ª Dose', 'Única', 'Dose')
            GROUP BY DATA) AS VACINACAO_MS,
            (SELECT SUM(VACINACAO_D2) AS D2_APLICADAS FROM VIEW_VACINACAO GROUP BY DATA) AS VACINACAO_DIVE,
            (SELECT SUM(LEITOS_ATIVOS) AS LEITOS_ATIVOS, SUM(LEITOS_OCUPADOS) AS LEITOS_OCUPADOS FROM leitoscovid 
            WHERE ATUALIZACAO = (SELECT MAX(ATUALIZACAO) FROM leitoscovid) GROUP BY ATUALIZACAO) AS LEITOS_COVID, 
            (SELECT SUM(LEITOS_ATIVOS) AS LEITOS_ATIVOS, SUM(LEITOS_OCUPADOS) AS LEITOS_OCUPADOS FROM leitosgeraiscovid 
            WHERE ATUALIZACAO = (SELECT MAX(ATUALIZACAO) FROM leitosgeraiscovid) GROUP BY ATUALIZACAO) AS LEITOS_GERAL
        WHERE RT_REGIONAL.REGIONAL = CASOS.REGIONAL
            AND RT_REGIONAL.DATA = CASOS.DATA
            AND CASOS_ATUAL.ID = RT_REGIONAL.REGIONAL
            AND CASOS_ANTERIOR.ID = RT_REGIONAL.REGIONAL
            AND VIEW_INCIDENCIA.ID  = RT_REGIONAL.REGIONAL
            AND RT_REGIONAL.REGIONAL = 1
            AND RT_REGIONAL.DATA = (SELECT MAX(DATA) FROM RT_REGIONAL)
        '''
        return self.__consultar(sql, ['id'])

    def buscar_dados_por_data(self,data):
        sql = """SELECT 
            RT_REGIONAIS.ID,
            RT_REGIONAIS.REGIONAL_SAUDE,
            RT_REGIONAIS.DATA,
            RT_REGIONAIS.RT,
            TABELA_REGIONAIS.LETALIDADE,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            TABELA_REGIONAIS.INCIDENCIA,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            ((VACINACAO.VACINACAO_D2::REAL / VACINACAO.POPULACAO) * 100) AS D2_PERCENTUAL,
            (LEITOS_REGIONAIS.LEITOS_OCUPADOS::NUMERIC / LEITOS_REGIONAIS.LEITOS_ATIVOS_MAX::NUMERIC * 100) AS OCUPACAO_LEITOS,
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
            AND RT_REGIONAIS.ID = {}
        ORDER BY RT_REGIONAIS.ID, RT_REGIONAIS.DATA
        """.format(str(data))

        return self.__consultar(sql)

    def busca_ultima_avaliacao(self):
        sql = '''SELECT ID,
                FASE_CALCULADA AS FASE_ANTERIOR,
                DATA_MUDANCA_FASE
            FROM "avaliacaoRegionais"
            WHERE DATA_CALCULO = (SELECT MAX(DATA_CALCULO) FROM "avaliacaoRegionais")
        '''
        return self.__consultar(sql, ['id'])
