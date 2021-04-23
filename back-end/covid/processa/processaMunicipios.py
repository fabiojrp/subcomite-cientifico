from covid.processa.dados import tabelas
from covid.processa.dao.DadosDao import DadosDao


class processaMunicipios:
    diasMediaMovel = 0
    diasVariacaoMediaMovel = 0
    tabelasDados = None

    def __init__(self, diasMMovel=7, diasVMovel=14):
        self.diasMediaMovel = diasMMovel
        self.diasVariacaoMediaMovel = diasVMovel
        self.tabelasDados = tabelas.Tabelas()
        self.DadosDao = DadosDao()
        return

    def processamento(self, dict_municipios):
        for municipio, linha in dict_municipios.items():
            print('Municipio : ', municipio, "..",
                  end='', flush=True)
            sumMediaMovelcasos = 0
            sumMediaMovelobitos = 0
            sumMediaMovelcasos3dias = 0
            sumMediaMovelobitos3dias = 0
            valores = {}
            listaDatas = list(linha["datas"].items())
            for i in range(0, len(listaDatas)):
                valores[i] = dict(
                    casos_acumulados=0,
                    obitos_acumulados=0,
                    casos_mediaMovel=0,
                    obitos_mediaMovel=0,
                    variacao_mediaMovel_casos=0,
                    casos_acumulados_100mil=0,
                    obitos_acumulados_100mil=0,
                    casos_variacao_14dias=0,
                    obitos_variacao_14dias=0,
                    incidencia_casos_diarios_100mil=0,
                    incidencia_obitos_diarios_100mil=0,
                    letalidade_100_confirmados=0,
                    incidencia_100mil=0,
                    dt_letalidade=0,
                    casos_ativos=0
                )

                if i > 0:

                    if listaDatas[i][1]['casos'] < 0:

                        try:
                            listaDatas[i+1][1]['casos'] += listaDatas[i][1]['casos']
                            listaDatas[i][1]['casos'] = 0
                        except Exception as error:
                            listaDatas[i][1]['casos'] = 0

                    # Casos e óbitos acumulados
                    valores[i]['casos_acumulados'] = listaDatas[i][1]['casos'] + \
                        valores[i-1]['casos_acumulados']
                    valores[i]['obitos_acumulados'] = listaDatas[i][1]['obitos'] + \
                        valores[i-1]['obitos_acumulados']

                    # Casos e óbitos por 100mil/habitantes
                    valores[i]['casos_acumulados_100mil'] = (
                        valores[i]['casos_acumulados'] / self.tabelasDados.getPopulacaoMunicipio(municipio))*100000
                    valores[i]['obitos_acumulados_100mil'] = (
                        valores[i]['obitos_acumulados']/self.tabelasDados.getPopulacaoMunicipio(municipio))*100000

                    # Incidencia por 100 mil
                    # casos
                    if listaDatas[i][1]['casos'] == 0:
                        valores[i]['incidencia_casos_diarios_100mil'] = 0.00000
                    else:
                        valores[i]['incidencia_casos_diarios_100mil'] = listaDatas[i][1]['casos'] * \
                            100000 / \
                            self.tabelasDados.getPopulacaoMunicipio(municipio)

                    # obitos
                    if listaDatas[i][1]['obitos'] == 0:
                        valores[i]['incidencia_obitos_diarios_100mil'] = 0.00000
                    else:
                        valores[i]['incidencia_obitos_diarios_100mil'] = listaDatas[i][1]['obitos'] * \
                            100000 / \
                            self.tabelasDados.getPopulacaoMunicipio(municipio)

                if i >= self.diasMediaMovel:
                    # Adiciona o valor atual e remove o valor mais antigo
                    sumMediaMovelcasos += listaDatas[i][1]['casos']
                    sumMediaMovelcasos -= listaDatas[i -
                                                     self.diasMediaMovel][1]['casos']

                    sumMediaMovelobitos += listaDatas[i][1]['obitos']
                    sumMediaMovelobitos -= listaDatas[i -
                                                      self.diasMediaMovel][1]['obitos']

                    valores[i]['casos_mediaMovel'] = sumMediaMovelcasos / \
                        self.diasMediaMovel
                    valores[i]['obitos_mediaMovel'] = sumMediaMovelobitos / \
                        self.diasMediaMovel

                else:
                    sumMediaMovelcasos += listaDatas[i][1]['casos']
                    sumMediaMovelobitos += listaDatas[i][1]['obitos']

                if i >= self.diasVariacaoMediaMovel-1:
                    # variação de casos 14 dias
                    if listaDatas[i][1]['casos'] == 0 or listaDatas[i-self.diasVariacaoMediaMovel][1]['casos'] == 0:
                        variacaoCasos = 0.00000
                    else:
                        variacaoCasos = (
                            listaDatas[i][1]['casos']/listaDatas[i-self.diasVariacaoMediaMovel][1]['casos'] - 1)*100

                    # variação de obitos 14 dias
                    if listaDatas[i][1]['obitos'] == 0 or listaDatas[i-self.diasVariacaoMediaMovel][1]['obitos'] == 0:
                        variacaoObitos = 0.00000
                    else:
                        variacaoObitos = (
                            listaDatas[i][1]['obitos']/listaDatas[i-self.diasVariacaoMediaMovel][1]['obitos']-1)*100

                    valores[i]['casos_variacao_14dias'] = variacaoCasos
                    valores[i]['obitos_variacao_14dias'] = variacaoObitos

                    # variação de casos da media movel
                    if valores[i]['casos_mediaMovel'] == 0 or valores[i-self.diasVariacaoMediaMovel]['casos_mediaMovel'] == 0:
                        variacaoCasosMediaMovel = 0.00000
                    else:
                        variacaoCasosMediaMovel = (
                            valores[i]['casos_mediaMovel']/valores[i-self.diasVariacaoMediaMovel]['casos_mediaMovel'] - 1)*100

                    valores[i]['variacao_mediaMovel_casos'] = variacaoCasosMediaMovel
            print("Ok")
            for i in range(0, len(listaDatas)):
                parametros = [
                    municipio,
                    linha['populacao'],
                    linha['regional'],
                    listaDatas[i][0],
                    listaDatas[i][1]['casos'],
                    listaDatas[i][1]['obitos'],
                    valores[i]['casos_acumulados'],
                    valores[i]['obitos_acumulados'],
                    valores[i]['casos_mediaMovel'],
                    valores[i]['obitos_mediaMovel'],
                    valores[i]['variacao_mediaMovel_casos'],
                    valores[i]['casos_acumulados_100mil'],
                    valores[i]['obitos_acumulados_100mil'],
                    valores[i]['casos_variacao_14dias'],
                    valores[i]['obitos_variacao_14dias'],
                    valores[i]['incidencia_casos_diarios_100mil'],
                    valores[i]['incidencia_obitos_diarios_100mil'],
                    #   data_sintoma,
                    valores[i]['dt_letalidade'],
                    #   dados['obitos_acumulados'],
                    #   dados['obitos_acumulados'],
                    #   dados['casos_acumulados'],
                    valores[i]['casos_ativos']
                ]

                self.DadosDao.casos_municipio(parametros)


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
