import csv
import pandas as pd
import os

def pontuacaoRegiao(row):
    pontos = 0
    if row['id'] == 1:
        return 0;

    if row['rt'] <= 1: # RT menor ou igual a 1
        pontos += 5
    if row['ocupacao_leitos'] <= 60: # Ocupação de leitos menor do que 60%
        pontos += 5         
    if row['var_media_movel'] <= 15: # Variação média móvel menor do que 15%
        pontos += 5
    if row['letalidade'] <= row['letalidade_sc']: # Letalidade comparada com o estado
        pontos += 2
    if row['incidencia'] <= row['incidencia_sc']: # Incidência comparada com o estado
        pontos += 2
    
    f = pontuacaoVacinas[row['fase_anterior']]['eval'] # Verifica qual a fase a regional está e atribui a função de comparação
    if (f(row['vacinacao_d2'])): # Verifica a vacinação conforme percentual de vacinação
        pontos += 3

    return pontos

dir_path = os.getcwd() + \
    '/back-end/covid/processa/indicadores/'
with open(dir_path + 'boletins.csv', 'r') as arquivo:
    df = pd.read_csv(arquivo, sep= ';')

    # Corta as colunas em que todos os campos foram NAN
    df = df.dropna(axis=1, how='all')

    #  converte todos os valores para números
    df['ocupacao_leitos'] = df['ocupacao_leitos'] .apply(pd.to_numeric, errors='coerce')

    # Substitui o que for NA.
    df = df.fillna('')

    print(df.head(2))

    pontuacaoVacinas = {
        1.0: {'proximo': 2.0, 'eval': lambda a: a < 0.2},
        2.0: {'proximo': 3.1, 'eval': lambda a: a > 0.2},
        3.1: {'proximo': 3.2, 'eval': lambda a: a > 0.3},
        3.2: {'proximo': 3.3, 'eval': lambda a: a > 0.4},
        3.3: {'proximo': 4.0, 'eval': lambda a: a > 0.5},
        4.0: {'proximo': '',  'eval': lambda a: a > 0.75},
        '':  {'proximo': '',  'eval': lambda a: a > 1},
    }

    df['pontuacao'] = df.apply(pontuacaoRegiao, axis=1)
    df['fase_anterior'] = df.apply(
        lambda row: pontuacaoVacinas[row['fase_anterior']]['proximo']  if row['pontuacao'] >= 15
               else row['fase_anterior'], axis=1)

    print(df.head(1))


