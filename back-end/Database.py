import psycopg2


class Database:

    conn = None
    instance = None

    @staticmethod
    def get_instance():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def __init__(self, host='localhost',port='5432', user='postgres', password='WEpJqsYMnHWB', dbname='covid'):

        try:
            conn = psycopg2.connect(
                host=host,port=port, user=user, password=password, dbname=dbname)
            conn.autocommit = True
            self.conn = conn
            print(self.conn)

        except psycopg2.Error as error:
            print(error)
            
            
            # if error.errno == errorcode.ER_BAD_DB_ERROR:
            #     print("Database doesn't exist")
            # elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            #     print("User name or password is wrong")
            # else:
            #     print(errorcode)

    def execute_query(self, query, params=None):
        curs = self.conn.cursor()
        curs.execute(query, params)
        return curs
    
    def execute_many_regionais(self,params):
        sql = """INSERT INTO regionais values (%s,%s,%s)"""
        curs = self.conn.cursor()
        curs.executemany(sql, params)  
        return curs
    
    def execute_many_municipios(self,params):
        sql = """INSERT INTO municipios values (%s,%s,%s,%s)"""
        curs = self.conn.cursor()
        curs.executemany(sql, params)   
        return curs 

    def execute_many_ibge(self,params):
        sql = """INSERT INTO ibge values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        curs = self.conn.cursor()   
        curs.executemany(sql, params)  
        return curs
