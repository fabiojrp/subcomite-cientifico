import sys
import os
from covid.processa.dao.Database import Database
from covid.processa.beans.EntidadeGeografica import EntidadeGeografica
from covid.processa.processaRegiao import processaRegiao


class TestadorBD:

    def __init__(self):
        self.db = Database.get_instance()

    def getMaxData(self, sql_data, params):

        curs = self.db.conn.cursor()
        curs.execute(sql_data, (params,))

        data = curs.fetchone()

        return data

    def getCasosPorRegional(self, sql, params):
        curs = self.db.conn.cursor()
        curs.execute(sql, params)

        rows = curs.fetchall()

        retornoBD = [EntidadeGeografica() for x in range(len(rows))]

        for row, entiGeo in zip(rows, retornoBD):

            entiGeo.setRegional_saude(row[0])
            entiGeo.setData(row[1])
            entiGeo.setMediaMovel(row[2])

        return retornoBD

    # def getCasosPorRegional2(self, params):
        #sql = """SELECT * FROM mediamovel_carlos where regional = %s and media_movel is not null order by data;"""

        #curs = self.db.conn.cursor()
        #curs.execute(sql, params)

        #rows = curs.fetchall()

        #retornoBD = [EntidadeGeografica() for x in range(len(rows))]

        # for row, entiGeo in zip(rows, retornoBD):

        # entiGeo.setRegional_saude(row[0])
        # entiGeo.setData(row[1])
        # entiGeo.setMediaMovel(row[2])

        # return retornoBD

    def getCasosPorMunicipio(self, sql, params):
        curs = self.db.conn.cursor()
        curs.execute(sql, params)

        rows = curs.fetchall()

        retornoBD = [EntidadeGeografica() for x in range(len(rows))]

        for row, entiGeo in zip(rows, retornoBD):

            entiGeo.setRegional_saude(row[0])
            entiGeo.setCodigo_ibge_municipio(row[1])
            entiGeo.setData(row[2])
            entiGeo.setMediaMovel(row[3])

        return retornoBD

    def salvarOutputsMunicipioNoBD(self, municipio, isCompletlyRT):

        sql = """INSERT INTO rt_municipio VALUES(%s,%s,%s,%s)"""

        for datas in municipio:
            if isCompletlyRT:
                # print(datas.getMediaMovel())
                params = [datas.getRegional_saude(),
                          datas.getCodigo_ibge_municipio(),
                          datas.getData(),
                          datas.getRt()]

                self.db.execute_query(sql, params)
                self.db.conn.commit()
            else:
                if municipio.index(datas) >= 31:

                    # print(datas.getMediaMovel())
                    params = [datas.getRegional_saude(),
                              datas.getCodigo_ibge_municipio(),
                              datas.getData(),
                              datas.getRt()]

                    self.db.execute_query(sql, params)
                    self.db.conn.commit()

                else:
                    continue

    def salvarOutputsRegionalNoBD(self, regional, isCompletlyRT, regional_id):

        processa_regiao = processaRegiao()

        sql = """INSERT INTO rt_regional VALUES(%s,%s,%s)"""

        # regionais_rt = {}

        # regionais_rt[regional_id] = list()
        # regionais_rt['datas'] = list()

        if isCompletlyRT:
            for datas in regional:
                index = regional.index(datas)
                # print(datas.getMediaMovel())
                params = [datas.getRegional_saude(),
                          datas.getData(),
                          datas.getRt()]

                self.db.execute_query(sql, params)
                self.db.conn.commit()

                # regionais_rt[regional_id].insert(index, datas.getRt())
                # regionais_rt['datas'].insert(index, datas.getData())

        else:
            for datas in regional:
                index = regional.index(datas)
                if index >= 30:
                    # print(datas.getMediaMovel())
                    params = [datas.getRegional_saude(),
                              datas.getData(),
                              datas.getRt()]

                    self.db.execute_query(sql, params)
                    self.db.conn.commit()

                    # regionais_rt[regional_id].insert(index - 30, datas.getRt())
                    # regionais_rt['datas'].insert(index - 30, datas.getData())

                else:
                    continue

    # def salvarOutputsRegionalNoBD2(self, regional, isCompletlyRT, regional_id):

        #processa_regiao = processaRegiao()

        #sql = """INSERT INTO rt_regional_teste VALUES(%s,%s,%s)"""

        #regionais_rt = {}

        #regionais_rt[regional_id] = list()
        #regionais_rt['datas'] = list()

        # if isCompletlyRT:
            # for datas in regional:
                #index = regional.index(datas)
                # print(datas.getMediaMovel())
                # params = [datas.getRegional_saude(),
                    # datas.getData(),
                    # datas.getRt()]

                #self.db.execute_query(sql, params)
                # self.db.conn.commit()

                #regionais_rt[regional_id].insert(index, datas.getRt())
                #regionais_rt['datas'].insert(index, datas.getData())

        # else:
            # for datas in regional:
                #index = regional.index(datas)
                # if index >= 30:
                    # print(datas.getMediaMovel())
                    # params = [datas.getRegional_saude(),
                    # datas.getData(),
                    # datas.getRt()]

                    #self.db.execute_query(sql, params)
                    # self.db.conn.commit()

                    #regionais_rt[regional_id].insert(index - 30, datas.getRt())
                    #regionais_rt['datas'].insert(index - 30, datas.getData())

                # else:
                    # continue

        # return regionais_rt
