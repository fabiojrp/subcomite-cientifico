import tabula


class extrair:
    def getDadosFormato1(file_path):
        area = (170, 27, 382, 570)
        df = tabula.read_pdf(file_path, pages='7')

        tabula.convert_into(file_path, "output.csv", output_format="csv", pages='7', area=area,
                            columns=[124, 175, 223, 271, 320, 370, 417, 468, 515])

    def getDadosFormato2(file_path):
        area = (170, 27, 382, 570)
        df = tabula.read_pdf(file_path, output_format="json", pages='4', area=area, columns=[
                             124, 175, 223, 271, 320, 370, 417, 468, 515])
        print(df)
        # tabula.convert_into(file_path, "output.csv", output_format="csv", pages='7', area=area,
        # columns=[124, 175, 223, 271, 320, 370, 417, 468, 515])
        df[0]['data'][4]
        df[0]['data'][6]

    def getDadosRegionais(_self, file_path, paginas):
        area = [[200, 9, 300, 155],
                [358, 137, 416, 570],
                [515, 9, 615, 155],
                [668, 137, 727, 570]]

        df = tabula.read_pdf(file_path, output_format="json",
                             pages=paginas,
                             area=area,
                             columns=[150, 220, 296, 338, 391, 434, 484, 531])
        if len(df) != 16:
            raise Exception('Quantidade de dados das Regiões não correspondem')
        # print(df)

        dados_leitos = []
        for i in range(0, int(len(df)/2)):
            regional = (' '.join([str(x[0]['text']) for x in df[i*2]['data']]))
            dia_regional = {'regional': regional,
                            'total': {
                                'ativos': int(df[i*2+1]['data'][0][1]['text']) + 
                                    int(df[i*2+1]['data'][1][1]['text']) + 
                                    int(df[i*2+1]['data'][2][1]['text']),
                                'ocupados_covid': int(df[i*2+1]['data'][0][1]['text']),
                                'ocupados_outros': int(df[i*2+1]['data'][1][1]['text']),
                                'livres': int(df[i*2+1]['data'][2][1]['text'])
                            },
                            'adulto': {
                                'ativos': int(df[i*2+1]['data'][0][3]['text']) + 
                                    int(df[i*2+1]['data'][1][3]['text']) + 
                                    int(df[i*2+1]['data'][2][3]['text']),
                                'ocupados_covid': int(df[i*2+1]['data'][0][3]['text']),
                                'ocupados_outros': int(df[i*2+1]['data'][1][3]['text']),
                                'livres': int(df[i*2+1]['data'][2][3]['text'])
                            }
                            }
            dados_leitos.append(dia_regional)

        return dados_leitos

    def getDadosSC(_self, file_path, pagina):
        area = (220, 128, 320, 570)
        colunas = [128, 175, 223, 271, 320, 370, 417, 468, 515]
        df = tabula.read_pdf(file_path, output_format="json",
                             pages=pagina,
                             area=area,
                             columns=colunas)
        if len(df[0]['data']) != 2 or len(df[0]['data'][0]) != 10:
            raise Exception('Quantidade de dados do Estado de SC não correspondem')
        dadosSC = {'regional': 'Estado SC',
                            'Internações em UTI': {
                                'SUS':{
                                    'Confirmados': int(df[0]['data'][0][1]['text']),
                                    'Suspeitos': int(df[0]['data'][0][2]['text']),
                                    'Total': int(df[0]['data'][0][3]['text']),
                                },
                                'Rede Privada':{
                                    'Confirmados': int(df[0]['data'][0][4]['text']),
                                    'Suspeitos': int(df[0]['data'][0][5]['text']),
                                    'Total': int(df[0]['data'][0][6]['text']),
                                },
                                'Total':{
                                    'Confirmados': int(df[0]['data'][0][7]['text']),
                                    'Suspeitos': int(df[0]['data'][0][8]['text']),
                                    'Total': int(df[0]['data'][0][9]['text']),
                                },

                            },
                            'Ventilação mecânica': {
                                'SUS':{
                                    'Confirmados': int(df[0]['data'][1][1]['text']),
                                    'Suspeitos': int(df[0]['data'][1][2]['text']),
                                    'Total': int(df[0]['data'][1][3]['text']),
                                },
                                'Rede Privada':{
                                    'Confirmados': int(df[0]['data'][1][4]['text']),
                                    'Suspeitos': int(df[0]['data'][1][5]['text']),
                                    'Total': int(df[0]['data'][1][6]['text']),
                                },
                                'Total':{
                                    'Confirmados': int(df[0]['data'][1][7]['text']),
                                    'Suspeitos': int(df[0]['data'][1][8]['text']),
                                    'Total': int(df[0]['data'][1][9]['text']),
                                }
                            }
                            
                    }
        return dadosSC

        # tabula.convert_into(file_path, "output2.csv", output_format="csv", pages=paginas, area=area)
