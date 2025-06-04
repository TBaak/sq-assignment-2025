import os
import sqlite3
from sqlite3 import Error

from Enum.Color import Color
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


class DBRepository:

    db_filename = "database.db"
    db_dir = "../../../Storage"

    @staticmethod
    def create_connection():
        conn = None

        base_dir = os.path.dirname(os.path.realpath(__file__))

        if not os.path.exists(os.path.realpath(base_dir + DBRepository.db_dir)):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Database opslag fout, afsluiten...", Color.FAIL),
                1
            )
            exit(1)

        try:
            db_file = os.path.realpath(base_dir + DBRepository.db_dir + "/" + DBRepository.db_filename)
            conn = sqlite3.connect(db_file)
        except Error as e:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Database fout, afsluiten...", Color.FAIL),
                1
            )
            exit(1)
        return conn