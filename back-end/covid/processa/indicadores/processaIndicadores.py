import pandas as pd
import os
from datetime import datetime
from covid.processa.indicadores.daoIndicadores import daoIndicadores
# from daoIndicadores import daoIndicadores

class processaIndicadores:

    def __init__(self):
        self.dao = daoIndicadores()
        self.pontuacaoVacinas = {
            1.0: {'proximo': 2.0, 'eval': lambda a: a >= 20},
            2.0: {'proximo': 3.1, 'eval': lambda a: a >= 30},
            3.1: {'proximo': 3.2, 'eval': lambda a: a >= 40},
            3.2: {'proximo': 3.3, 'eval': lambda a: a >= 50},
            3.3: {'proximo': 4.0, 'eval': lambda a: a >= 75},
            4.0: {'proximo': 4.0, 'eval': lambda a: a >= 75},
            '':  {'proximo': '',  'eval': lambda a: a >= 100},
        }
        self.pontuacaoVacinasBD = {
            1.0: {'proximo': 2.0, 'eval': lambda a: a > 0.20},
            2.0: {'proximo': 3.1, 'eval': lambda a: a >= 0.30},
            3.1: {'proximo': 3.2, 'eval': lambda a: a >= 0.40},
            3.2: {'proximo': 3.3, 'eval': lambda a: a >= 0.50},
            3.3: {'proximo': 4.0, 'eval': lambda a: a >= 0.75},
            4.0: {'proximo': 4.0, 'eval': lambda a: a >= 1},
            '':  {'proximo': '',  'eval': lambda a: a >= 1},
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

    def __pontuacaoRegiaoBD(self, row):
        pontos = 0
        if row['rt'] <= 1: # RT menor ou igual a 1
            pontos += 5
        if row['leitos_covid_max'] <= 0.60 or row['leitos_geral_max'] <= 0.60: # Ocupação de leitos menor do que 60%
            pontos += 5         
        if row['var_media_movel'] <= 0.15: # Variação média móvel menor do que 15%
            pontos += 5
        if row['letalidade'] <= row['letalidade_sc']: # Letalidade comparada com o estado
            pontos += 2
        if row['incidencia'] <= row['incidencia_sc']: # Incidência comparada com o estado
            pontos += 2
        
        f = self.pontuacaoVacinasBD[row['fase_anterior']]['eval'] # Verifica qual a fase a regional está e atribui a função de comparação
        if (f(row['vacinacao_d2_dive']) or f(row['vacinacao_d2_ms'])): # Verifica a vacinação conforme percentual de vacinação
                pontos += 3


        return pontos

    def __mudancaFase(self, row):
        if row['pontuacao'] >= 15 and \
                self.__days_between(row['data_mudanca_fase'], row['data']) >= 14 and \
                row['ocupacao_leitos'] < 80:
            return pd.Series([self.pontuacaoVacinas[row['fase_anterior']]['proximo'], row['data']])
        else:
            return pd.Series([row['fase_anterior'], row['data_mudanca_fase']])
        
    def __mudancaFaseBD(self, row):
        if row['pontuacao'] >= 15 and \
                self.__days_between(row['data_mudanca_fase'], row['data']) >= 14 and \
                (row['leitos_covid_max'] < 80 or row['leitos_geral_max'] < 80):
            return pd.Series([self.pontuacaoVacinas[row['fase_anterior']]['proximo'], row['data']])
        else:
            return pd.Series([row['fase_anterior'], row['data_mudanca_fase']])


    def __days_between(self, d1, d2):
        # d1 = datetime.strptime(d1, "%Y-%m-%d")
        # d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    
    # def __days_betweenBD(self, d1, d2):
    #     d1 = datetime.strptime(d1, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    #     return abs((d2 - d1).days)


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

            #ajusta as datas
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date
            df['data_mudanca_fase'] = pd.to_datetime(df['data_mudanca_fase'], errors='coerce').dt.date

            # Substitui o que for NA.
            df = df.fillna('')

            df['pontuacao'] = df.apply(self.__pontuacaoRegiao, axis=1)
            
            df[['fase_calculada', 'data_mudanca_fase']] = df.apply(
                lambda row: [self.pontuacaoVacinas[row['fase_anterior']]['proximo'], row['data']]  if row['pontuacao'] >= 15 and self.__days_between(row['data_mudanca_fase'], row['data']) >= 14
                else [row['fase_anterior'], row['data_mudanca_fase']], 
                axis=1, result_type="expand")
            
            # ajustando para os dados retirados do BD:
            df = df.rename(columns={"ocupacao_leitos": "leitos_geral_max", "vacinacao_d2": "vacinacao_d2_dive"})
            df = df.drop(['vacinacao_d1'], axis=1);
            df['leitos_covid_max'] = '';
            df['vacinacao_d2_ms'] = '';


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

            #ajusta a data
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date

            # busca os dados da semana anterior e junta com os dados atuais
            df = pd.concat([df, self.dao.busca_ultima_avaliacao()], axis=1)
            
            # Calcula a pontuação
            df['pontuacao'] = df.apply(self.__pontuacaoRegiao, axis=1)

            # Aplica a fase calculada
            df[['fase_calculada', 'data_mudanca_fase']] = df.apply(self.__mudancaFase, axis=1)

            #ajusta as datas
            df['data_mudanca_fase'] = pd.to_datetime(df['data_mudanca_fase'], errors='coerce').dt.date
            
            # ajustando para os dados retirados do BD:
            df = df.rename(columns={"ocupacao_leitos": "leitos_geral_max", "vacinacao_d2": "vacinacao_d2_dive"})
            df = df.drop(['vacinacao_d1'], axis=1);
            df['leitos_covid_max'] = '';
            df['vacinacao_d2_ms'] = '';

            self.dao.salvaBD(df)

    def processaIndicadoresBD(self):     
        df = self.dao.buscar_dados_atuais()

        # busca os dados da semana anterior e junta com os dados atuais
        df = pd.concat([df, self.dao.busca_ultima_avaliacao()], axis=1)
        
        #ajusta a data
        df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date

        # Calcula a pontuação
        df['pontuacao'] = df.apply(self.__pontuacaoRegiaoBD, axis=1)

        # Aplica a fase calculada
        df[['fase_calculada', 'data_mudanca_fase']] = df.apply(self.__mudancaFaseBD, axis=1)
        
        self.dao.salvaBD(df)


# if __name__ == "__main__":
#     processaIndicadores = processaIndicadores()
#     processaIndicadores.processaIndicadoresPrimeiroArquivo('boletim (08-07).csv');
#     processaIndicadores.processaIndicadoresArquivos('boletim (15-07).csv')  
#     processaIndicadores.processaIndicadoresArquivos('boletim (22-07).csv')
#     processaIndicadores.processaIndicadoresArquivos('boletim (29-07).csv')  
#     processaIndicadores.processaIndicadoresArquivos('boletim (05-08).csv')  
#     processaIndicadores.processaIndicadoresArquivos('boletim (12-08).csv')
#     processaIndicadores.processaIndicadoresArquivos('boletim (19-08).csv')
#     # processaIndicadores.processaIndicadoresBD()