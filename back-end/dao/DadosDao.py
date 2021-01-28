import json
from dao.Dao import Dao
from dados.tabelas import Tabelas

tabelas = Tabelas();

class DadosDao(Dao):

    def insert(self, params):
        sql = """
            INSERT INTO dados ( 
                data_publicacao,
                recuperados,
                data_inicio_sintomas,
                data_coleta,
                sintomas,
                comorbidades,
                gestante,
                internacao,
                internacao_uti,
                sexo,
                municipio,
                obito,
                data_obito,
                idade,
                regional,
                raca,
                data_resultado,
                codigo_ibge_municipio,
                latitude,
                longitude,
                estado,
                criterio_confirmacao,
                tipo_teste,
                municipio_notificacao,
                codigo_ibge_municipio_notificacao,
                latitude_notificacao,
                longitude_notificacao,
                classificacao,
                origem_esus,
                origem_sivep,
                origem_lacen,
                origem_laboratorio_privado,
                nom_laboratorio,
                fez_teste_rapido,
                fez_pcr,
                data_internacao,
                data_entrada_uti,
                regional_saude,
                data_evolucao_caso,
                data_saida_uti,
                bairro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
        """

        self.db.execute_query(sql, params)
        self.db.conn.commit()
	
    def insertBrasil(self, params):
        sql = """
            INSERT INTO CASOSBRASIL ( 
                regiao,
                estado,
                municipio,
                coduf,
                codmun,
                codRegiaoSaude,
                nomeRegiaoSaude,
                data,
                semanaEpi,
                populacaoTCU2019,
                casosAcumulado,
                casosNovos,
                obitosAcumulado,
                obitosNovos,
                Recuperadosnovos,
                emAcompanhamentoNovos,
                interior_metropolitana
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
        """

        self.db.execute_query(sql, params)
        self.db.conn.commit()
    
    def casos_municipios(self, dict_municipios):
        index = 0;
        #with open('casos.json', 'w') as arquivo_casos:
        #    json.dump(dict_municipios, arquivo_casos)
        #print(json.dumps(dict_municipios, indent=4))
        for municipio, linha in dict_municipios.items():
            #print('Municipio : ', municipio)
            index = index + 1
            regional = linha['regional']
            for data_sintoma, dados in linha['datas'].items():
                sql = """INSERT INTO casos(
                    codigo_ibge_municipio,
                    populacao,
                    regional,
                    data,
                    casos, 
                    obitos,
                    casos_acumulados,
                    obitos_acumulados,
                    casos_mediaMovel,
                    obitos_mediaMovel,
                    casos_variacao_14dias,
                    obitos_variacao_14dias,
                    casos_acumulados_100mil,
                    obitos_acumulados_100mil,
                    incidencia_casos_diarios_100mil,
                    incidencia_obitos_diarios_100mil,
                    letalidade_100_confirmados,
                    casos_ativos
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (case when %s < %s or %s = 0 then 0.00000 
                                else (cast(%s as numeric(10,5))/cast(%s as numeric(10,5))) end), %s)"""
                dt_letalidade = tabelas.getDataLetalidadeRegional(regional)
                parametros = [municipio, 
                        linha['populacao'],
                        regional, 
                        data_sintoma, 
                        dados['casos'], 
                        dados['obitos'], 
                        dados['casos_acumulados'], 
                        dados['obitos_acumulados'],
                        dados['casos_mediaMovel'],
                        dados['obitos_mediaMovel'],
                        dados['casos_variacao_14dias'],
                        dados['obitos_variacao_14dias'],
                        dados['casos_acumulados_100mil'],
                        dados['obitos_acumulados_100mil'],
                        dados['incidencia_casos_diarios_100mil'],
                        dados['incidencia_obitos_diarios_100mil'],
                        data_sintoma,
                        dt_letalidade,
                        dados['obitos_acumulados'],
                        dados['obitos_acumulados'],
                        dados['casos_acumulados'],
                        dados['casos_ativos']
                ]
                self.db.execute_query(sql, parametros)
                self.db.conn.commit()

                # sql = """UPDATE casos SET letalidade_100_confirmados = 
                #             (case when data < %s or obitos_acumulados = 0 then 0.00000 
                #                 else (cast(obitos_acumulados as numeric(10,5))/cast(casos_acumulados as numeric(10,5))) end) where codigo_ibge_municipio = %s and data = %s"""
                
                # parametros = [dt_letalidade,
                #         municipio,
                #         data_sintoma
                # ]
                # self.db.execute_query(sql, parametros)
                # self.db.conn.commit()

                #print("\t\t", key2, ' : ', value2)
             
                index = index + 1
                if index % 100000 == 0:
                    print(index, flush=True)
                elif index % 10000 == 0:
                    print(index, end='', flush=True)
                elif index % 1000 == 0:
                    print('.', end='', flush=True)
        print('Fim', flush=True)
	
    def leitos_hospitais(self, params):
	sql = """
	    INSERT INTO leitos ( 
		macrorregiao,
		hospital,
		municipio,
		codigo_ibge_municipio,
		regional_saude,
		leitos_ativos,
		leitos_ocupados,
		leitos_disponiveis,
		taxa_ocupacao,
		pacientes_covid
	    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
	"""

	self.db.execute_query(sql, params)
	self.db.conn.commit()
        ''' 

         ## SQL para obter casos  por município:
        SELECT regionais.regional_saude, casos.data, 
            sum(casos.populacao) as populacao,
            sum(casos.casos) as casos_dia, 
            sum(casos.obitos) as obitos_dias,
            sum(casos.casos_acumulados) as casos_acumulados, 
            sum(casos.obitos_acumulados) as obitos_acumulados,
            to_char(sum(casos.casos_mediaMovel), '99990d999999') as casos_mediaMovel, 
            to_char(sum(casos.obitos_mediaMovel), '99990d999999') as obitos_mediaMovel,
            to_char(avg(casos.casos_acumulados_100mil), '99990d999999') as casos_acumulados_100mil, 
            to_char(avg(casos.obitos_acumulados_100mil), '99990d999999') as obitos_acumulados_100mil
        FROM regionais, casos 
        where casos.regional = regionais.id group by regionais.regional_saude, casos.data
		


        


        ## SQL para obter casos totais por município:
        SELECT ibge.municipio, sum(casos.casos) as total FROM covid.casos, covid.ibge 
        WHERE casos.codigo_ibge_municipio = ibge.cod_municipio 
        GROUP by casos.codigo_ibge_municipio ORDER BY  total desc	
    
        
        # SQL Totais por região
        SELECT regionais.regional_saude, sum(casos.casos), sum(casos.obitos) FROM regionais, casos 
        where casos.regional = regionais.id group by regionais.regional_saude

        Casos floripa:
        SELECT * FROM covid.casos where casos.codigo_ibge_municipio = "4205407";
       

        # SQL totais por dia por região
       SELECT regionais.regional_saude, casos.data, 
            sum(casos.populacao) as populacao,
            sum(casos.casos) as casos_dia, 
            sum(casos.obitos) as obitos_dias,
            sum(casos.casos_acumulados) as casos_acumulados, 
            sum(casos.obitos_acumulados) as obitos_acumulados,
            to_char(sum(casos.casos_mediaMovel), '99990d999999') as casos_mediaMovel, 
            to_char(sum(casos.obitos_mediaMovel), '99990d999999') as obitos_mediaMovel,
            to_char(avg(casos.casos_acumulados_100mil), '99990d999999') as casos_acumulados_100mil, 
            to_char(avg(casos.obitos_acumulados_100mil), '99990d999999') as obitos_acumulados_100mil
        FROM regionais, casos 
        where casos.regional = regionais.id group by regionais.regional_saude, casos.data
		
        #SQL ativos em Videira
        select * from dados where municipio = 'VIDEIRA' and (obito = 'NAO' and recuperados = 'NAO')


        '''


    def exibe_alertas(self):
        self.db.execute_query("SHOW WARNINGS")
        self.db
