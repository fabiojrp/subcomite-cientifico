from ..dao.Dao import DadosDao

class comandosSql:

    def __init__(self):
        self.dadosDao = DadosDao()

    def casos_municipios(self, dict_municipios):
        return None


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
		
        
        #Media móvel
SELECT REGIONAIS.REGIONAL_SAUDE,
	CASOS.DATA,
	SUM(CASOS.CASOS) AS CASOS_DIA,
	SUM(CASOS.OBITOS) AS OBITOS_DIAS,
	TO_CHAR(SUM(CASOS.CASOS_MEDIAMOVEL),'99990d999999') AS CASOS_MEDIAMOVEL,
	TO_CHAR(SUM(CASOS.OBITOS_MEDIAMOVEL),'99990d999999') AS OBITOS_MEDIAMOVEL
FROM REGIONAIS, CASOS
WHERE DATA BETWEEN NOW() - interval '14 days' AND NOW()
    AND CASOS.REGIONAL = REGIONAIS.ID
GROUP BY REGIONAIS.REGIONAL_SAUDE, CASOS.DATA 
    ORDER BY REGIONAIS.REGIONAL_SAUDE


            # Casos Blumenau
        SELECT * FROM casos where casos.codigo_ibge_municipio = '4202404';


        '''