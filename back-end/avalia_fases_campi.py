import schedule
import time
import pandas as pd
import sys
import os
import numpy as np

from avaliacao.dao import *
from datetime import datetime

fases = {
    0: "Fase 1",
    1: "Fase 2",
    2: "Fase 3.1",
    3: "Fase 3.2",
    4: "Fase 3.2",
    5: "Fase 3.3",
    6: "Fase 4"
}

# APTO A MELHORAR
def pontuacao_por_fase(df_dados):
    if ((df_dados[16] == 0 and df_dados[15] >= 20) or \
        (df_dados[16] == 1 and df_dados[15] >= 30) or \
        (df_dados[16] == 2 and df_dados[15] >= 40) or \
        (df_dados[16] == 3 and df_dados[15] >= 50)):
        return 3
    else:
        return 0

# APTO A MELHORAR
def aplica_fase(df_avaliado):
    df_avaliado['fase_atual'] = [fases[regional[3]+1] if regional[2] >= 15 else fases[regional[3]] for regional in df_avaliado.values]
    df_avaliado['id_fase'] = [regional[3]+1 if regional[2] >= 15 else regional[3] for regional in df_avaliado.values]
    
    
def calcula_pontos(df_avaliacao, df_dados):
    df_avaliacao['pontos'] += [5 if x <= 1 else 0 for x in df_dados['rt_valor']]
    df_avaliacao['pontos'] += [5 if x <= 60 else 0 for x in df_dados['leitos_ocupados']]
    df_avaliacao['pontos'] += [5 if x <= 15 else 0 for x in df_dados['variacao']]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['letalidade'], df_dados['letalidade_sc'])]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['incidencia'], df_dados['incidencia_sc'])]
    df_avaliacao['pontos'] += [pontuacao_por_fase(x) for x in df_dados.values]
    
    if df_avaliacao['pontos'] >= 15:
        df_avaliacao['isAdvancing'] = True
        df_avaliacao['isRegressing'] = False
    elif df_avaliacao['pontos'] > 5:
        df_avaliacao['isAdvancing'] = False
        df_avaliacao['isRegressing'] = False
    else:
        df_avaliacao['isAdvancing'] = False
        df_avaliacao['isRegressing'] = True


def normaliza_avaliacao(df_dados_atuais, df_ultima_avaliacao):
    df_avaliacao = pd.DataFrame()
    
    df_avaliacao['id'] = df_dados_atuais['id']
    df_avaliacao['regionais'] = df_dados_atuais['regionais']
    df_avaliacao['pontos'] = 0

    calcula_pontos(df_avaliacao, df_dados_atuais)
    df_avaliacao.insert(3, 'id_fase', (df_ultima_avaliacao['id_fase'] if df_ultima_avaliacao['id_fase'] else 1 ))
    aplica_fase(df_avaliacao)
    df_avaliacao['created_at'] = pd.to_datetime(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%d %H:%M"))
    
    return df_avaliacao


def avaliacao(df_dados, df_ultima_avaliacao):
    if df_ultima_avaliacao == None:
        pass

def avaliacao_completa():
    data_inicio = datetime.datetime(2021, 7, 21)
    data_fim = datetime.datetime.today()
    data_quarta = data_inicio
    
    df_ultima_avaliacao = None
    while True:
        df_dados = buscar_dados_por_data(data_quarta)
        df_avaliacao = normaliza_avaliacao(df_dados, df_ultima_avaliacao)
        
        data_quarta = data_quarta + datetime.timedelta(7)
        df_ultima_avaliacao = busca_ultima_avaliacao()
        if data_quarta > data_fim:
            break
            

def avaliar_regionais():
    try:
        ultima_avaliacao = busca_ultima_avaliacao()
    except Exception as error:
        ultima_avaliacao = avaliacao_completa()
        
    # if ultima_avaliacao == None:
    #     pass
    # else:
    #     df_dadosAtuais = dados_atual()
        
    df_avaliacao = normaliza_avaliacao(df_dadosAtuais)
    print(df_avaliacao)
    

avaliar_regionais()







# Avalia as resgionais quando é quarta, ás 23:59
# schedule.every().wednesday.at("23:59").do(avaliar_campi)


# while True:
#     schedule.run_pending()
#     time.sleep(1)