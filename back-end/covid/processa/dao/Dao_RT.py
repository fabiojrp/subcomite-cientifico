from .Database import Database


class Dao_RT:
    def __init__(self):
        self.db = Database.get_instance()

    def create_table(self):
        print("Limpando e recriando a tabela RT")
        # Limpa as tabelas
        self.db.execute_query("DROP VIEW IF EXISTS VIEW_RT")
        self.db.execute_query("DROP TABLE IF EXISTS rt")

        sql = """
            CREATE TABLE IF NOT EXISTS rt (
                   regional integer DEFAULT NULL,
                   data date DEFAULT NULL,
                   rt NUMERIC(17,5) DEFAULT NULL
               )
        """
        self.db.execute_query(sql)

        sql = """CREATE VIEW view_rt AS SELECT REGIONAIS.REGIONAL_SAUDE,
                    REGIONAIS.ID,
                    REGIONAIS.POLIGONO::JSONB,
                    REGIONAIS.URL AS URL,
                    RT_REGIONAL.DATA AS DATA,
                    RT_REGIONAL.VALOR_R AS RT
                FROM REGIONAIS, RT_REGIONAL
                WHERE RT_REGIONAL.DATA = (SELECT MAX(RT_REGIONAL.DATA) FROM RT_REGIONAL)
                                AND RT_REGIONAL.REGIONAL = REGIONAIS.ID
                ORDER BY REGIONAIS.REGIONAL_SAUDE,
                    RT_REGIONAL.DATA
        """

        # sql = """CREATE VIEW view_rt AS SELECT REGIONAIS.REGIONAL_SAUDE,
        #             REGIONAIS.ID,
        #             REGIONAIS.POLIGONO::JSONB,
        #             REGIONAIS.URL AS URL,
        #             RT.DATA AS DATA,
        #             RT.RT AS RT
        #         FROM REGIONAIS, RT
        #         WHERE RT.DATA = (SELECT MAX(RT.DATA) FROM RT)
        #                         AND RT.REGIONAL = REGIONAIS.ID
        #         ORDER BY REGIONAIS.REGIONAL_SAUDE,
        #             RT.DATA
        # """
        self.db.execute_query(sql)

    def insert_value_rt(self, params):
        sql = """INSERT INTO rt VALUES (%s,%s,%s)"""
        self.db.execute_query(sql, params)
        self.db.conn.commit()

    def insert_value_rt2(self, params):
        sql = """INSERT INTO rt VALUES (%s,%s)"""
        self.db.execute_query(sql, params)
        self.db.conn.commit()

    def buscaDatas(self):
        curs = self.db.conn.cursor()
        curs.execute("SELECT DISTINCT(data) FROM rt_regional ORDER BY data")
        return curs.fetchall()

    def buscaDadosRegionais(self, regional):
        curs = self.db.conn.cursor()
        curs.execute(
            "SELECT * FROM rt_regional WHERE regional = %s ORDER BY data", (regional,))
        return curs.fetchall()
