from Database import Database


class Dao:
    def __init__(self):
        self.db = Database.get_instance()
