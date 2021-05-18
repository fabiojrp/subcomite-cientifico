import tabula

class processa:
    def getDadosFormato1(file_path):
        area =  (170, 27, 382, 570)
        df = tabula.read_pdf(file_path, pages='7')  

        tabula.convert_into(file_path, "output.csv", output_format="csv", pages='7', area=area, 
            columns=[124, 175, 223, 271, 320, 370, 417, 468, 515])

    def getDadosFormato2(file_path):
        area =  (170, 27, 382, 570)
        df = tabula.read_pdf(file_path, output_format="json", pages='4', area=area, columns=[124, 175, 223, 271, 320, 370, 417, 468, 515])  
        print(df)
        # tabula.convert_into(file_path, "output.csv", output_format="csv", pages='7', area=area, 
            # columns=[124, 175, 223, 271, 320, 370, 417, 468, 515])
        df[0]['data'][4]
        df[0]['data'][6]

    def getRegionais(file_path):
        area =  [ [200, 9, 300, 155],
            [358, 137, 416, 570], 
            [515, 9, 615, 155],
            [668, 137, 727, 570]]
        
        df = tabula.read_pdf(file_path, output_format="json", 
            pages=[5, 6, 7, 8], 
            area=area,
            columns=[150, 220, 296, 338, 391, 434, 484, 531])  
        if len(df) != 16:
            print ("Erro processando: " + file_path)
        # print(df)
    
        dados_leitos = []
        for i in range(0, int(len(df)/2)):
            regional = (' '.join([str(x[0]['text']) for x in df[i*2]['data']]))
            dia_regional = {'regional': regional,
                            'leitos': {
                                'ocupados_covid' : int(df[i*2+1]['data'][0][3]['text']),
                                'ocupados_outros' : int(df[i*2+1]['data'][1][3]['text']),
                                'livres': int(df[i*2+1]['data'][2][3]['text'])
                            }
            }
            dados_leitos.append(dia_regional)
        print(dados_leitos)


    def tabulaSC(file_path):
        area =  (430, 27, 430+361, 570)
        df = tabula.read_pdf(file_path, pages='7')  

        tabula.convert_into(file_path, "output2.csv", output_format="csv", pages='7', area=area)

