import mysql
from mysql.connector import errorcode


class Database:

    conn = None
    instance = None

    @staticmethod
    def get_instance():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def __init__(self, host='localhost', user='root', password='WEpJqsYMnHWB', db='covid'):

        try:
            conn = mysql.connector.connect(
                host=host, user=user, password=password, db=db)
            conn.autocommit = True
            self.conn = conn

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password is wrong")
            else:
                print(errorcode)

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor() 
        cursor.execute(query, params)
        return cursor
