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
def pontuacao_vacinacao_por_fase(df_dados):
    if ((df_dados[3] == 0 and df_dados[8] >= 20) or \
        (df_dados[3] == 1 and df_dados[8] >= 30) or \
        (df_dados[3] == 2 and df_dados[8] >= 40) or \
        (df_dados[3] == 3 and df_dados[8] >= 50) or \
        (df_dados[3] == 4 and df_dados[8] >= 75)):
        return 3
    else:
        return 0

# APTO A MELHORAR
def aplica_fase(df_avaliacao, df_ultima_avaliacao):
    if df_ultima_avaliacao == None or not df_ultima_avaliacao['hasAdvanced']: 
        df_avaliacao[df_avaliacao['pontos'] >= 15] \
            ['hasAdvanced'] = True \
            ['id_fase'] = [regional+1 if regional >= 15 else regional for regional in ['id_fase']] \
            ['fase_atual'] = [fases[x] for x in ['id_fase']]
        
        df_avaliacao[df_avaliacao['pontos'] > 5] \
            ['hasAdvanced'] = False \
            ['hasRegressed'] = False
        
        df_avaliacao[df_avaliacao['pontos'] <= 5] \
            ['hasAdvanced'] = False \
            ['hasRegressed'] = True \
            ['fase_atual'] = [fases[regional[3] - 1] if regional[3] >= 15 and fases[regional[3] - 1] >= 0 else fases[regional[3]] for regional in df_avaliacao.values] \
            ['id_fase'] = [regional[3] - 1 if regional[3] >= 15 and fases[regional[3] - 1] >= 0 else regional[3] for regional in df_avaliacao.values]
    else:
        pass
        
        
def calcula_pontos(df_avaliacao, df_dados):
    df_avaliacao['pontos'] += [5 if x <= 1 else 0 for x in df_dados['rt']]
    df_avaliacao['pontos'] += [5 if x <= 60 else 0 for x in df_dados['ocupacao_leitos']]
    df_avaliacao['pontos'] += [5 if x <= 15 else 0 for x in df_dados['variacao']]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['letalidade'], df_dados['letalidade_sc'])]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['incidencia'], df_dados['incidencia_sc'])]
    df_avaliacao['pontos'] += [pontuacao_vacinacao_por_fase(x) for x in df_dados.values]


def normaliza_avaliacao(df_dados_atuais, df_ultima_avaliacao):
    df_avaliacao = pd.DataFrame()
    print(df_dados_atuais)
    
    df_avaliacao['id'] = df_dados_atuais['id']
    df_avaliacao['regionais'] = df_dados_atuais['regional_saude']
    df_avaliacao['pontos'] = 0
    df_avaliacao.insert(3, 'id_fase', (df_ultima_avaliacao['id_fase'] if df_ultima_avaliacao else 0 ))
    df_avaliacao['hasAdvanced'] = False
    df_avaliacao['hasRegressed'] = False
    
    calcula_pontos(df_avaliacao, df_dados_atuais)
    aplica_fase(df_avaliacao, df_ultima_avaliacao)
    df_avaliacao['created_at'] = pd.to_datetime(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%d %H:%M"))
    
    return df_avaliacao


def avaliacao_completa():
    data_inicio = datetime(2021, 7, 28)
    data_fim = datetime.today()
    data_quarta = data_inicio
    
    df_ultima_avaliacao = None
    while True:
        df_dados = buscar_dados_por_data(data_quarta.strftime('%Y-%m-%d'))
        df_avaliacao = normaliza_avaliacao(df_dados, df_ultima_avaliacao)
        
        print(df_avaliacao)
        
        data_quarta = data_quarta + datetime.timedelta(7)
        df_ultima_avaliacao = busca_ultima_avaliacao()
        if data_quarta > data_fim:
            break
            

def avaliar_regionais():
    avaliacao_completa()
    

avaliar_regionais()







# Avalia as resgionais quando é quarta, ás 23:59
# schedule.every().wednesday.at("23:59").do(avaliar_campi)


# while True:
#     schedule.run_pending()
#     time.sleep(1)