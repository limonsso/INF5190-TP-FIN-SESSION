import sqlite3


class TpInf5190Db:

    def __init__(self):
        self.connection = None

    def get_connection(self, db_file='./db/tpinf5190.db'):
        if self.connection is None:
            self.connection = sqlite3.connect(db_file)
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
