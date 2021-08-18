import sys
import os
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import psycopg2

config = {
    "host": "localhost",
    "port": 5432,
    "dbname": "covid",
    "user": "postgres",
    "password": "!admpasswd@covid"
}

def get_connection():
    try:
        conn = psycopg2.connect(**config)
        return conn
    except:
        print('Não é possível estabelecar conexão com o banco de dados.')
        sys.exit(1)


def get_engine():
    my_config = {}
    my_config['drivername'] = "postgresql"
    my_config['username'] = config['user']
    my_config['password'] = config['password']
    my_config['port'] = str(config['port'])
    my_config['host'] = str(config['host'])
    my_config['database'] = str(config['dbname'])
    url = URL(**my_config)
    return create_engine(url)


def consultar(sql):
    conn = get_connection()
    data = pd.read_sql_query(sql, conn)
    return data

def buscar_dados_atuais():
    
    sql = '''
    SELECT VIEW_RT.REGIONAL_SAUDE AS REGIONAIS,
            VIEW_RT.ID AS ID, 
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO,
            VIEW_RT.DATA AS RT_DATA,
            VIEW_RT.RT AS RT_VALOR,
            VIEW_RT.poligono AS POLIGONO,
            VIEW_RT.url AS url,
            (VIEW_LEITOS_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_OCUPADOS,
            VIEW_LEITOS_MAX.DATA AS LEITOS_DATA, 
            VIEW_CASOS_ATUAL.DATA AS DATA_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR.DATA AS DATA_CASOS_ANTERIOR,
            VIEW_INCIDENCIA.INCIDENCIA,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            VIEW_INCIDENCIA.LETALIDADE,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            view_vacinacao.vacinacao_d2 / view_vacinacao.populacao AS D2_DIVE
            --(VIEW_VACINACAO_MS_POR_REGIAO.D2 / VIEW_VACINACAO_MS_POR_REGIAO.POPULACAO) AS D2_MS
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS_MAX,
            VIEW_INCIDENCIA,
            view_vacinacao,
            --VIEW_VACINACAO_MS_POR_REGIAO,
            (SELECT VIEW_INCIDENCIA.LETALIDADE, VIEW_INCIDENCIA.INCIDENCIA
                FROM VIEW_INCIDENCIA
                WHERE VIEW_INCIDENCIA.ID  = 1) as TABELA_ESTADO
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
            AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
            AND VIEW_RT.ID = VIEW_LEITOS_MAX.ID
            AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
            --AND VIEW_RT.ID = VIEW_VACINACAO_MS_POR_REGIAO.ID
            AND VIEW_RT.ID = view_vacinacao.ID	
            AND VIEW_LEITOS_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_MAX)
            --AND VIEW_VACINACAO_MS_POR_REGIAO.DATA = (SELECT MAX(DATA) FROM VIEW_VACINACAO_MS_POR_REGIAO)
    '''
    return consultar(sql)

def buscar_dados_totais():
    sql = '''
    
    '''
    return consultar(sql)

def busca_ultima_avaliacao():
    sql = '''
    SELECT 
        * 
    FROM AVALIACAO_REGIONAIS
        WHERE CREATED_AT = (SELECT NOW() - INTERVAL '7 DAYS')
    '''
    return consultar(sql)