import sqlite3
from sqlite3 import Error


class Repository:

    @staticmethod
    def create_connection():
        conn = None
        try:
            db_file = "database.db"
            conn = sqlite3.connect(db_file)
        except Error as e:
            raise e # TODO: handle error
        return conn