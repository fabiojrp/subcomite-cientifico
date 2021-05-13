class processaRegiao:
    @staticmethod
    def buscaNomeRegiao(regiao_id):
        # Tabela de regionais
        regional = {
            1: 'SANTA CATARINA',
            2: 'Alto Uruguai Catarinense',
            3: 'Alto Vale do Itajaí',
            4: 'Alto Vale do Rio do Peixe',
            5: 'Carbonífera',
            6: 'Extremo Oeste',
            7: 'Extremo Sul Catarinense',
            8: 'Foz do Rio Itajaí',
            9: 'Grande Florianópolis',
            10: 'Laguna',
            11: 'Médio Vale do Itajaí',
            12: 'Meio Oeste',
            13: 'Nordeste',
            14: 'Oeste',
            15: 'Planalto Norte',
            16: 'Serra Catarinense',
            17: 'Xanxerê'
        }
        try:
            regional = regional[regiao_id]
        except KeyError as ex:
            print("!--- Erro processando: {", regiao_id, "} ---!")
            regional = -1
        return regional

    @staticmethod
    def buscaNomeRegiaoPlanilha(regiao_id):
        # Tabela de regionais
        regional = {
            0: 'Região da Saúde',
            1: 'SANTA CATARINA',
            2: 'Alto Uruguai Catarinense',
            3: 'Alto Vale do Itajaí',
            4: 'Alto Vale do Rio do Peixe',
            5: 'Carbonífera',
            6: 'Extremo Oeste',
            7: 'Extremo Sul Catarinense',
            8: 'Foz do Rio Itajaí',
            9: 'Grande Florianópolis',
            10: 'Laguna',
            11: 'Médio Vale do Itajaí',
            12: 'Meio Oeste',
            13: 'Nordeste',
            14: 'Oeste',
            15: 'Planalto Norte',
            16: 'Serra Catarinense',
            17: 'Xanxerê'
        }
        try:
            regional = regional[regiao_id]
        except KeyError as ex:
            print("!--- Erro processando: {", regiao_id, "} ---!")
            regional = -1
        return regional

    @staticmethod
    def buscaCampusRegiaoPlanilha(regiao_id):
        # Tabela dos campi
        regional = {
            0: 'Instituto Federal Catarinense',
            1: 'ESTADO',
            2: 'Concórdia',
            3: 'Ibirama e Rio do Sul',
            4: 'Fraiburgo e Videira',
            5: '',
            6: '',
            7: 'Santa Rosa do Sul e Sombrio',
            8: 'Camboriú',
            9: '',
            10: '',
            11: 'Blumenau e Brusque',
            12: 'Luzerna',
            13: 'Araquari e São Francisco do Sul',
            14: '',
            15: 'São Bento do Sul',
            16: '',
            17: 'Abelardo Luz'
        }
        try:
            regional = regional[regiao_id]
        except KeyError as ex:
            print("!--- Erro processando: {", regiao_id, "} ---!")
            regional = -1
        return regional
