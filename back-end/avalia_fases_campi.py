import schedule
import time
import pandas as pd
import sys
import os
import numpy as np

from avaliacao.dao import *
import datetime

fases = {
    0: "Fase 1",
    1: "Fase 2",
    2: "Fase 3.1",
    3: "Fase 3.2",
    4: "Fase 3.3",
    5: "Fase 4"
}

# APTO A MELHORAR
def pontuacao_vacinacao_por_fase(id, d2):
    if ((id == 0 and d2 >= 20) or \
        (id == 1 and d2 >= 30) or \
        (id == 2 and d2 >= 40) or \
        (id == 3 and d2 >= 50) or \
        (id == 4 and d2 >= 75)):
        return 3
    else:
        return 0


def aplica_fase(df_avaliacao, df_ultima_avaliacao):
    if (df_ultima_avaliacao.empty) : 
        df_avaliacao['hasAdvanced'] = (df_avaliacao['pontos'] >= 15) & (~df_avaliacao['isLocked'])
        # COM REGRESSÃO
        # df_avaliacao['hasRegressed'] = df_avaliacao['pontos'] < 5
        df_avaliacao['id_fase'] += [1 if reg_adv else 0 for reg_adv in df_avaliacao['hasAdvanced']]    
        df_avaliacao['fase_atual'] = [fases[id_fase] for id_fase in df_avaliacao['id_fase']]
    else:
        df_avaliacao['hasAdvanced'] = (~df_ultima_avaliacao['hasAdvanced']) & (df_avaliacao['pontos'] >= 15) & (~df_avaliacao['isLocked'])
        # COM REGRESSÃO
        # df_avaliacao['hasRegressed'] = df_avaliacao['pontos'] < 5
        df_avaliacao['id_fase'] += [1 if reg_adv else 0 for reg_adv in df_avaliacao['hasAdvanced']]   
        df_avaliacao['fase_atual'] = [fases[id_fase] for id_fase in df_avaliacao['id_fase']]
        
        
        
def calcula_pontos(df_avaliacao, df_dados):
    df_avaliacao['pontos'] += [5 if x <= 1 else 0 for x in df_dados['rt']]
    df_avaliacao['pontos'] += [5 if x <= 60 else 0 for x in df_dados['ocupacao_leitos']]
    df_avaliacao['pontos'] += [5 if x <= 15 else 0 for x in df_dados['variacao']]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['letalidade'], df_dados['letalidade_sc'])]
    df_avaliacao['pontos'] += [2 if x <= y else 0 for x,y in zip(df_dados['incidencia'], df_dados['incidencia_sc'])]
    df_avaliacao['pontos'] += [pontuacao_vacinacao_por_fase(id, d2) for id, d2 in zip(df_dados['id_fase'], df_dados['d2_percentual'])]


def faz_avaliacao(df_dados_atuais, df_ultima_avaliacao):
    df_avaliacao = pd.DataFrame()
    df_avaliacao['id'] = df_dados_atuais['id']
    df_avaliacao['regionais'] = df_dados_atuais['regional_saude']
    df_avaliacao['data_avaliacao'] = df_dados_atuais['data']
    df_avaliacao['id_fase'] = (0 if df_ultima_avaliacao.empty else df_ultima_avaliacao['id_fase'])
    df_avaliacao['pontos'] = 0
    df_avaliacao['hasAdvanced'] = False
    df_avaliacao['hasRegressed'] = False
    df_avaliacao['isLocked'] = df_dados_atuais['ocupacao_leitos'] >= 80
    
    df_dados_atuais['id_fase'] = df_avaliacao['id_fase']
    
    calcula_pontos(df_avaliacao, df_dados_atuais)
    aplica_fase(df_avaliacao, df_ultima_avaliacao)
    return df_avaliacao


def avaliacao_completa():
    data_inicio = datetime.datetime(2021, 7, 28)
    data_fim = datetime.datetime.today() - datetime.timedelta(7)
    data_quarta = data_inicio
    
    df_avaliacao_completa = pd.DataFrame()
    df_ultima_avaliacao = pd.DataFrame()
    while True:
        
        df_dados = buscar_dados_por_data(data_quarta.strftime('%Y-%m-%d'))
        df_avaliacao = faz_avaliacao(df_dados, df_ultima_avaliacao)
        
        salvaBD(df_avaliacao)
        
        data_quarta = data_quarta + datetime.timedelta(7)
        df_ultima_avaliacao = busca_ultima_avaliacao()
        
        if data_quarta > data_fim:
            break


# def avaliacao_semanal(df_ultima_avaliacao):
#     data_avaliacao = datetime.datetime.today()
#     df_dados = buscar_dados_por_data(data_avaliacao)
#     df_avaliacao = faz_avaliacao(df_dados, df_ultima_avaliacao)
#     salvaBD(df_avaliacao)

def avaliar_regionais():
    avaliacao_completa()


if __name__ == '__main__':
    avaliar_regionais()







# Avalia as resgionais quando é quarta, ás 23:59
# schedule.every().wednesday.at("23:59").do(avaliar_campi)


# while True:
#     schedule.run_pending()
#     time.sleep(1)