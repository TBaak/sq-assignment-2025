import sqlite3
from sqlite3 import Error

from Enum.Color import Color
from View.UserInterfaceFlow import UserInterfaceFlow


class DBRepository:

    dbFilename = "database.db"

    @staticmethod
    def create_connection():
        conn = None
        try:
            db_file = DBRepository.dbFilename
            conn = sqlite3.connect(db_file)
        except Error as e:
            UserInterfaceFlow.quick_run(
                UserInterfaceFlow("Database fout, afsluiten...", Color.FAIL),
                1
            )
            exit(1)
        return conn