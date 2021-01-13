from dados import tabelas

class estatistica:
  diasMediaMovel = 0
  diasVariacaoMediaMovel = 0
  tabelasDados = None;
  def __init__(self, diasMMovel = 7, diasVMovel = 14):
    self.diasMediaMovel = diasMMovel
    self.diasVariacaoMediaMovel = diasVMovel
    self.tabelasDados = tabelas.Tabelas()
    return

  def processamento(self, dict_municipios):
    for municipio, linha in dict_municipios.items():
      #print('Municipio : ', municipio)
      sumMediaMovelcasos = 0
      sumMediaMovelobitos = 0
      sumMediaMovelcasos3dias = 0
      sumMediaMovelobitos3dias = 0

      listaDatas = list(linha["datas"].items())

      for i in range(0, len(listaDatas)):

          if i > 0:
            #Casos e óbitos acumulados
            listaDatas[i][1]['casos_acumulados'] = listaDatas[i][1]['casos'] + listaDatas[i-1][1]['casos_acumulados']
            listaDatas[i][1]['obitos_acumulados'] = listaDatas[i][1]['obitos'] + listaDatas[i-1][1]['obitos_acumulados']
            
            #Casos e óbitos por 100mil/habitantes
            listaDatas[i][1]['casos_acumulados_100mil'] = (listaDatas[i][1]['casos_acumulados']/ self.tabelasDados.getPopulacaoMunicipio(municipio))*100000
            listaDatas[i][1]['obitos_acumulados_100mil'] = (listaDatas[i][1]['obitos_acumulados']/self.tabelasDados.getPopulacaoMunicipio(municipio))*100000

            #Incidencia por 100 mil
              #casos
            if listaDatas[i][1]['casos'] == 0:
              listaDatas[i][1]['incidencia_casos_diarios_100mil'] = 0.00000
            else:
              listaDatas[i][1]['incidencia_casos_diarios_100mil'] = listaDatas[i][1]['casos']*100000/self.tabelasDados.getPopulacaoMunicipio(municipio)

              #obitos
            if listaDatas[i][1]['obitos'] == 0:
              listaDatas[i][1]['incidencia_obitos_diarios_100mil'] = 0.00000
            else:
              listaDatas[i][1]['incidencia_obitos_diarios_100mil'] = listaDatas[i][1]['obitos']*100000/self.tabelasDados.getPopulacaoMunicipio(municipio)

          if i>= self.diasVariacaoMediaMovel-1:
            #variação de casos 14 dias
            if listaDatas[i][1]['casos'] == 0 or listaDatas[i-self.diasVariacaoMediaMovel][1]['casos'] == 0:
              variacaoCasos = 0.00000
            else:
              variacaoCasos = (listaDatas[i][1]['casos']/listaDatas[i-self.diasVariacaoMediaMovel][1]['casos'] -1)*100

            #variação de obitos 14 dias
            if listaDatas[i][1]['obitos'] == 0 or listaDatas[i-self.diasVariacaoMediaMovel][1]['obitos'] == 0:
              variacaoObitos = 0.00000
            else:
              variacaoObitos = (listaDatas[i][1]['obitos']/listaDatas[i-self.diasVariacaoMediaMovel][1]['obitos']-1)*100

            listaDatas[i][1]['casos_variacao_14dias'] = variacaoCasos
            listaDatas[i][1]['obitos_variacao_14dias'] = variacaoObitos

          #Média móvel
          if i >= self.diasMediaMovel-1:
            #Adiciona o valor atual e remove o valor mais antigo
            sumMediaMovelcasos += listaDatas[i][1]['casos']
            sumMediaMovelcasos -= listaDatas[i-self.diasMediaMovel+1][1]['casos']

            sumMediaMovelobitos += listaDatas[i][1]['obitos']
            sumMediaMovelobitos -= listaDatas[i-self.diasMediaMovel+1][1]['obitos']

            listaDatas[i][1]['casos_mediaMovel'] =  sumMediaMovelcasos/self.diasMediaMovel
            listaDatas[i][1]['obitos_mediaMovel'] = sumMediaMovelobitos/self.diasMediaMovel
            
          else:
            sumMediaMovelcasos += listaDatas[i][1]['casos']
            sumMediaMovelobitos += listaDatas[i][1]['obitos']


    return dict_municipios 
        

'''
Média móvel de casos confirmados 
Média móvel do número de óbitos 
Variação do número de casos semanal 
Taxa de letalidade (a partir de 100 casos) 
Casos ativos
Incidência por 100mil/habitantes.
Taxa de transmissibilidade R(t)
Ocupação de leitos de UTI


Proposta do Subcomitê:

Média móvel e variação do Número de Casos confirmados;
Taxa de letalidade em regiões com mais de 100 casos confirmados;
Taxa de ocupação de leitos de UTI;
Taxa de transmissibilidade R(t);
Número de casos confirmados acumulados por 100 mil habitantesI
'''
