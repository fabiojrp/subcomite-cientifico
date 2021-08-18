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

def pontuacao_por_fase(df_dados):
    if ((df_dados[16] == 0 and df_dados[15] >= 20) or \
        (df_dados[16] == 1 and df_dados[15] >= 30) or \
        (df_dados[16] == 2 and df_dados[15] >= 40) or \
        (df_dados[16] == 3 and df_dados[15] >= 50)):
        return 3
    else:
        return 0
    
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
    
def dados_atual():
    dados_last = buscar_dados_atuais()
    dados_last['leitos_ocupados'] *= 100
    dados_last['id_fase'] = 0
    
    return dados_last

def normaliza_avaliacao(dados_last):
    df_avaliacao = pd.DataFrame()
    
    df_avaliacao['id'] = dados_last['id']
    df_avaliacao['regionais'] = dados_last['regionais']
    df_avaliacao['pontos'] = 0
    
    calcula_pontos(df_avaliacao, dados_last)
    
    df_avaliacao.insert(3, 'id_fase', dados_last['id_fase'])
    
    aplica_fase(df_avaliacao)
    
    df_avaliacao['created_at'] = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%d %H:%M")

def avaliar_campi():
    try:
        ultima_avaliacao = busca_ultima_avaliacao()
    except Exception as error:
        ultima_avaliacao = None
        
    if ultima_avaliacao == None:
        pass
    else:
        df_dadosAtuais = dados_atual()
        
    df_avaliacao = normaliza_avaliacao(df_dadosAtuais)
    print(df_avaliacao)
    

avaliar_campi()







# Avalia as resgionais quando é quarta, ás 23:59
# schedule.every().wednesday.at("23:59").do(avaliar_campi)


# while True:
#     schedule.run_pending()
#     time.sleep(1)