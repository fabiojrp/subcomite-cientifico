class processaLeitos:

    def buscaInfoHospital(nome_hospital):
        # Tabela de regionais
        hospital = {
            'HOSPITAL E MAT. MARIETA K. BORNHAUSEN': {'municipio': 420820, 'index_regional': 8},
            'HOSPITAL MUNICIPAL RUTH CARDOSO': {'municipio': 420200, 'index_regional': 8},
            'CEPON': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL BEIRA MAR': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL DE CARIDADE': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL FLORIANÓPOLIS': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL GOVERNADOR CELSO RAMOS': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL INSTITUTO DE CARDIOLOGIA': {'municipio': 421660, 'index_regional': 9},
            'HOSPITAL NEREU RAMOS': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL NOSSA SENHORA DA IMACULADA CONCEICAO': {'municipio': 421150, 'index_regional': 9},
            'HOSPITAL REGIONAL DE BIGUACU HELMUTH NASS': {'municipio': 420230, 'index_regional': 9},
            'HOSPITAL REGIONAL SÃO JOSÉ': {'municipio': 421660, 'index_regional': 9},
            'HOSPITAL UNIVERSITÁRIO': {'municipio': 420540, 'index_regional': 9},
            'HOSPITAL REGIONAL DO OESTE': {'municipio': 420420, 'index_regional': 14},
            'HOSPITAL REGIONAL SÃO PAULO': {'municipio': 421950, 'index_regional': 17},
            'HOSPITAL SÃO JOSÉ MARAVILHA': {'municipio': 421050, 'index_regional': 6},
            'HOSPITAL TEREZINHA GAIO BASO': {'municipio': 421720, 'index_regional': 6},
            'HOSPITAL DIVINO SALVADOR': {'municipio': 421900, 'index_regional': 4},
            'HOSPITAL E MATERNIDADE TEREZA RAMOS': {'municipio': 420930, 'index_regional': 16},
            'HOSPITAL HELIO ANJO ORTIZ': {'municipio': 420480, 'index_regional': 4},
            'HOSPITAL MAICE': {'municipio': 420300, 'index_regional': 4},
            'HOSPITAL NOSSA SENHORA DOS PRAZERES': {'municipio': 420930, 'index_regional': 16},
            'HOSPITAL SANTA TEREZINHA': {'municipio': 420900, 'index_regional': 12},
            'HOSPITAL SÃO FRANCISCO': {'municipio': 420430, 'index_regional': 2},
            'HOSPITAL BETHESDA': {'municipio': 420910, 'index_regional': 13},
            'HOSPITAL E MATERNIDADE JARAGUÁ': {'municipio': 420890, 'index_regional': 13},
            'HOSPITAL MUNICIPAL SÃO JOSÉ JOINVILLE': {'municipio': 420910, 'index_regional': 13},
            'HOSPITAL REGIONAL HANS DIETER': {'municipio': 420910, 'index_regional': 13},
            'HOSPITAL SAGRADA FAMILIA': {'municipio': 421580, 'index_regional': 15},
            'HOSPITAL SANTA CRUZ': {'municipio': 420380, 'index_regional': 15},
            'HOSPITAL SÃO BRÁS': {'municipio': 421360, 'index_regional': 15},
            'HOSPITAL SÃO JOSÉ JARAGUA DO SUL': {'municipio': 420890, 'index_regional': 13},
            'HOSPITAL SÃO VICENTE DE PAULO': {'municipio': 421010, 'index_regional': 15},
            'HOSP. NOSSA SENHORA CONCEIÇÃO': {'municipio': 421870, 'index_regional': 10},
            'HOSPITAL DE CARIDADE S B J DOS PASSOS': {'municipio': 420940, 'index_regional': 10},
            'HOSPITAL DE RETAGUARDA RIO MAINA': {'municipio': 420460, 'index_regional': 5},
            'HOSPITAL REGIONAL ARARANGUÁ': {'municipio': 420140, 'index_regional': 7},
            'HOSPITAL SAO CAMILO': {'municipio': 420730, 'index_regional': 10},
            'HOSPITAL SÃO DONATO': {'municipio': 420700, 'index_regional': 5},
            'HOSPITAL SÃO JOSÉ CRICIUMA': {'municipio': 420460, 'index_regional': 5},
            'HOSPITAL AZAMBUJA': {'municipio': 420290, 'index_regional': 11},
            'HOSPITAL BEATRIZ RAMOS': {'municipio': 420750, 'index_regional': 11},
            'HOSPITAL BOM JESUS': {'municipio': 420850, 'index_regional': 3},
            'HOSPITAL DE GASPAR': {'municipio': 420590, 'index_regional': 11},
            'HOSPITAL OASE': {'municipio': 421820, 'index_regional': 11},
            'HOSPITAL REGIONAL ALTO VALE': {'municipio': 421480, 'index_regional': 3},
            'HOSPITAL SANTA ISABEL': {'municipio': 420240, 'index_regional': 11},
            'HOSPITAL SANTO ANTONIO': {'municipio': 420240, 'index_regional': 11},
            'HOSPITAL WALDOMIRO COLAUTTI': {'municipio': 420690, 'index_regional': 3},
            'HOSPITAL RIO NEGRINHO': {'municipio': 421500, 'index_regional': 15},
        }
        try:
            hospital = hospital[nome_hospital]
        except KeyError as ex:
            #print("!--- Hospital não encontrado: {", nome_hospital, "} ---!")
            hospital = -1
            raise Exception(
                "!--- Hospital não encontrado: {", nome_hospital, "} ---!")
        return hospital
