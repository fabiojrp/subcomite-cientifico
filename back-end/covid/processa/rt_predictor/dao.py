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
    "password": "xxxx"
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


def get_data_crescimento():
    sql = '''
    SELECT 
      REGIONAIS.regional_saude, 
      REGIONAIS.id, 
      RT_REGIONAL.DATA as data,
      RT_REGIONAL.VALOR_R as rt
    FROM REGIONAIS, RT_REGIONAL
    WHERE RT_REGIONAL.REGIONAL = REGIONAIS.ID AND REGIONAIS.ID <> 1
    ORDER BY REGIONAIS.REGIONAL_SAUDE, RT_REGIONAL.DATA
    '''
    return consultar(sql)


def get_data_gravidade():
    sql = '''
     SELECT 
      REGIONAIS.ID,
      REGIONAIS.REGIONAL_SAUDE,
      CASOS.DATA,      
      SUM(CASOS.OBITOS_ACUMULADOS) AS OBITOS_ACUMULADOS,     
      SUM(CASOS.CASOS_ACUMULADOS) AS CASOS_ACUMULADOS,      
      SUM(CASOS.POPULACAO) AS POPULACAO
     FROM REGIONAIS, CASOS
     WHERE CASOS.REGIONAL = REGIONAIS.ID
     AND REGIONAIS.ID <> 0 AND REGIONAIS.ID <> 1
     GROUP BY REGIONAIS.ID, REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
     ORDER BY REGIONAIS.ID, CASOS.DATA
    '''
    return consultar(sql)


def get_ml_data():
    df_crescimento = get_data_crescimento().dropna()
    df_gravidade = get_data_gravidade().dropna()

    periods = 7
    df = df_gravidade

    df['obitos_por_semana'] = df.groupby('regional_saude')[
        'obitos_acumulados'].diff(periods)

    df['obitos_por_semana/100k'] = df['obitos_por_semana'] / \
        (df['populacao'] / 100000)

    df['casos_por_semana'] = df.groupby('regional_saude')[
        'casos_acumulados'].diff(periods)

    df['casos_por_semana/100k'] = df['casos_por_semana'] / \
        (df['populacao'] / 100000)

    df_crescimento = df_crescimento[['data', 'regional_saude', 'rt']]
    df_gravidade = df_gravidade[['data', 'regional_saude',
                                'obitos_por_semana/100k', 'casos_por_semana/100k']]

    df = df_crescimento.merge(df_gravidade, how='left', on=[
        'data', 'regional_saude'])

    return df
