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
                                'ativos': int(df[i*2+1]['data'][0][1]['text'].replace(".", "")) + 
                                    int(df[i*2+1]['data'][1][1]['text'].replace(".", "")) + 
                                    int(df[i*2+1]['data'][2][1]['text'].replace(".", "")),
                                'ocupados_covid': int(df[i*2+1]['data'][0][1]['text'].replace(".", "")),
                                'ocupados_outros': int(df[i*2+1]['data'][1][1]['text'].replace(".", "")),
                                'livres': int(df[i*2+1]['data'][2][1]['text'].replace(".", ""))
                            },
                            'adulto': {
                                'ativos': int(df[i*2+1]['data'][0][3]['text'].replace(".", "")) + 
                                    int(df[i*2+1]['data'][1][3]['text'].replace(".", "")) + 
                                    int(df[i*2+1]['data'][2][3]['text'].replace(".", "")),
                                'ocupados_covid': int(df[i*2+1]['data'][0][3]['text'].replace(".", "")),
                                'ocupados_outros': int(df[i*2+1]['data'][1][3]['text'].replace(".", "")),
                                'livres': int(df[i*2+1]['data'][2][3]['text'].replace(".", ""))
                            }
                            }
            dados_leitos.append(dia_regional)

        return dados_leitos

    def getDadosRegionais2(_self, file_path, paginas):
        area = [ [175, 510, 175+80, 510+80],  [350, 504,  350+80, 504+80], [700, 509,  700+80, 509+80], 
                [700, 214,  700+80, 214+80],  [533, 213,  530+80, 216+80], [534, 508,  530+80, 510+70],
                [350, 204,  350+80, 204+80]]

        df = tabula.read_pdf(file_path, output_format="json",
                             pages=paginas,
                             area=area)
        if len(df) != 7:
            raise Exception('Quantidade de dados das Regiões não correspondem')
        # print(df)
        regionais = ['SANTA CATARINA (TOTAL)',  'GRANDE FLORIANÓPOLIS',  'FOZ DO RIO ITAJAÍ',  'GRANDE OESTE',  'MEIO OESTE E SERRA CATARINENSE',  'PLANALTO NORTE E NORDESTE',  'SUL',  'VALE DO ITAJAÍ']
        dados_leitos = []
        ocupados_covid = 0
        ocupados_outros = 0
        livres = 0
        dia_regional = {'regional': 'SANTA CATARINA (TOTAL)',
                            'total': {
                                'ativos': 0,
                                'ocupados_covid': 0,
                                'ocupados_outros': 0,
                                'livres': 0
                                },
                            'adulto': {
                                'ativos': "",
                                'ocupados_covid': "",
                                'ocupados_outros': "",
                                'livres': "",
                                }
                            }
        dados_leitos.append(dia_regional)

        for i in range(1, len(df)):
            try:
                ocupados_covid += int(df[i-1]['data'][0][0]['text'].replace(".", ""))
                ocupados_outros += int(df[i-1]['data'][1][0]['text'].replace(".", ""))
                livres += int(df[i-1]['data'][1][0]['text'].replace(".", ""))
                dia_regional = {'regional': regionais[i],
                                'total': {
                                    'ativos': int(df[i-1]['data'][0][0]['text'].replace(".", "")) + \
                                        int(df[i-1]['data'][1][0]['text'].replace(".", "")) + \
                                        int(df[i-1]['data'][2][0]['text'].replace(".", "")),
                                    'ocupados_covid': int(df[i-1]['data'][0][0]['text'].replace(".", "")),
                                    'ocupados_outros': int(df[i-1]['data'][1][0]['text'].replace(".", "")),
                                    'livres': int(df[i-1]['data'][2][0]['text'].replace(".", ""))
                                    },
                                'adulto': {
                                    'ativos': "",
                                    'ocupados_covid': "",
                                    'ocupados_outros': "",
                                    'livres': "",
                                    }
                                }
            except Exception as e:
                print("!!!Erro!!!")
                print(e);
                print("Arquivo: " + file_path + "Regional: " + regionais[i])
                dia_regional = {'regional': regionais[i],
                            'total': {
                                'ativos': 0,
                                'ocupados_covid': 0,
                                'ocupados_outros': 0,
                                'livres': 0
                                },
                            'adulto': {
                                'ativos': "",
                                'ocupados_covid': "",
                                'ocupados_outros': "",
                                'livres': "",
                                }
                            }
            finally:    
                dados_leitos.append(dia_regional)
        
        dados_leitos[0]['total']['ativos'] = ocupados_covid + ocupados_outros + livres
        dados_leitos[0]['total']['ocupados_covid'] = ocupados_covid
        dados_leitos[0]['total']['ocupados_outros'] = ocupados_outros
        dados_leitos[0]['total']['livres'] = livres
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
