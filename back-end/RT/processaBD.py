from Database import Database

class processaDB:
    def __init__(self):
        self.db = Database.get_instance()

    def create_table(self):
        print("Limpando e recriando a tabela RT")
        # Limpa as tabelas
        self.db.execute_query("DROP TABLE IF EXISTS rt")
        
        sql = """
            CREATE TABLE IF NOT EXISTS rt (
                   regional integer DEFAULT NULL,
                   data date DEFAULT NULL,
                   rt NUMERIC(17,5) DEFAULT NULL
               )
        """
        self.db.execute_query(sql)

            
    def insert_value_rt(self,params):
        sql = """INSERT INTO rt VALUES (%s,%s,%s)"""
        self.db.execute_query(sql, params)
        self.db.conn.commit()

    def insert_value_rt2(self,params):
        sql = """INSERT INTO rt VALUES (%s,%s)"""
        self.db.execute_query(sql, params)
        self.db.conn.commit()
