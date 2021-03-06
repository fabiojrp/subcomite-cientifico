import datetime

class processaDados:
      
    def buscaRegiao(self, regiao_nome):
         # Tabela de regionais
        regional = {
            'Ignorado':0,
            'SANTA CATARINA':1,
            'Alto Uruguai Catarinense':2,
            'Alto Vale do Itajaí ':3,
            'Alto Vale do Rio do Peixe':4,
            'Carbonífera':5,
            'Extremo Oeste':6,
            'Extremo Sul Catarinense':7,
            'Foz do Rio Itajaí':8,
            'Grande Florianópolis':9, 
            'Laguna':10,
            'Médio Vale do Itajaí':11,
            'Meio Oeste':12,
            'Nordeste':13,
            'Oeste':14,
            'Planalto Norte':15,
            'Serra Catarinense':16,
            'Xanxerê':17
        }
        try:
            regional = regional[regiao_nome]
        except KeyError as ex:
            print("!--- Erro processando: ", regiao_nome, " ---!")
            regional = -1
        return regional
        

    def date_format(self, date):
        if date == None:
            return -1

        return datetime.datetime.strptime(date, '%m/%d/%y').strftime("%Y-%m-%d")
        




