import pandas as pd
import os

from daoIndicadores import daoIndicadores

class processaIndicadores:

    def __init__(self):
        self.dao = daoIndicadores()
        self.pontuacaoVacinas = {
            1.0: {'proximo': 2.0, 'eval': lambda a: a < 0.2},
            2.0: {'proximo': 3.1, 'eval': lambda a: a > 0.2},
            3.1: {'proximo': 3.2, 'eval': lambda a: a > 0.3},
            3.2: {'proximo': 3.3, 'eval': lambda a: a > 0.4},
            3.3: {'proximo': 4.0, 'eval': lambda a: a > 0.5},
            4.0: {'proximo': 4.0,  'eval': lambda a: a > 0.75},
            '':  {'proximo': '',  'eval': lambda a: a > 1},
        }

    def __pontuacaoRegiao(self, row):
        pontos = 0
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
        
        f = self.pontuacaoVacinas[row['fase_anterior']]['eval'] # Verifica qual a fase a regional está e atribui a função de comparação
        if (f(row['vacinacao_d2'])): # Verifica a vacinação conforme percentual de vacinação
            pontos += 3

        return pontos

    def processaIndicadoresPrimeiroArquivo(self, filename):     

        dir_path = os.getcwd() + \
            '/covid/processa/indicadores/'
        with open(dir_path + filename, 'r') as arquivo:
            df = pd.read_csv(arquivo, sep= ';', index_col=[0])

            # Corta as colunas em que todos os campos foram NAN
            df = df.dropna(axis=1, how='all')

            #  converte todos os valores para números
            df['ocupacao_leitos'] = df['ocupacao_leitos'].apply(pd.to_numeric, errors='coerce')
            df['fase_anterior'] = df['fase_anterior'].astype('float64')
        
            # Substitui o que for NA.
            df = df.fillna('')

            df['pontuacao'] = df.apply(self.__pontuacaoRegiao, axis=1)

            df['fase_calculada'] = df.apply( lambda row: self.pontuacaoVacinas[row['fase_anterior']]['proximo']  if row['pontuacao'] >= 15 
                else row['fase_anterior'],  axis=1)
            
            self.dao.salvaBD(df, table='avaliacaoRegionais', type='replace')
        
        
    def processaIndicadoresArquivos(self, filename):     
        dir_path = os.getcwd() + \
            '/covid/processa/indicadores/'
        with open(dir_path + filename, 'r') as arquivo:
            df = pd.read_csv(arquivo, sep= ';', index_col=[0])

            # Corta as colunas em que todos os campos foram NAN
            df = df.dropna(axis=1, how='all')

            #  converte todos os valores para números
            df['ocupacao_leitos'] = df['ocupacao_leitos'].apply(pd.to_numeric, errors='coerce')

            # Substitui o que for NA.
            df = df.fillna('')

            # busca os dados da semana anterior e junta com os dados atuais
            df = pd.concat([df, self.dao.busca_ultima_avaliacao()], axis=1)
            
            # Calcula a pontuação
            df['pontuacao'] = df.apply(self.__pontuacaoRegiao, axis=1)

            # Aplica a fase calculada
            df['fase_calculada'] = df.apply(
                lambda row: self.pontuacaoVacinas[row['fase_anterior']]['proximo']  if row['pontuacao'] >= 15 
                else row['fase_anterior'], 
                axis=1)
            
            self.dao.salvaBD(df)


if __name__ == "__main__":
    processaIndicadores = processaIndicadores()
    processaIndicadores.processaIndicadoresPrimeiroArquivo('boletim (08-07).csv');
    processaIndicadores.processaIndicadoresArquivos('boletim (15-07).csv')  
    processaIndicadores.processaIndicadoresArquivos('boletim (22-07).csv')
    processaIndicadores.processaIndicadoresArquivos('boletim (29-07).csv')  
    processaIndicadores.processaIndicadoresArquivos('boletim (05-08).csv')  
    processaIndicadores.processaIndicadoresArquivos('boletim (12-08).csv')
    processaIndicadores.processaIndicadoresArquivos('boletim (19-08).csv')