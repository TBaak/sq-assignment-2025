import os
import sqlite3
from sqlite3 import Error

from Enum.Color import Color
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


class DBRepository:

    db_filename = "database.db"
    db_dir = "../../Storage"

    @staticmethod
    def create_connection(db_file=None, exit_on_error=True):
        if db_file is None:
            base_dir = os.path.dirname(os.path.realpath(__file__))
            db_folder = os.path.realpath(f"{base_dir}/{DBRepository.db_dir}")
            db_file = os.path.realpath(f"{db_folder}/{DBRepository.db_filename}")
            if not os.path.exists(db_folder):
                UserInterfaceFlow.quick_run(
                    UserInterfaceAlert("Database opslag fout, afsluiten...", Color.FAIL),
                    1
                )
                if exit_on_error:
                    exit(1)
                raise Error(f"Database file does not exist: {db_file}")

        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Database fout, afsluiten...", Color.FAIL),
                1
            )
            if exit_on_error:
                exit(1)
            raise Error(f"Could not connect to database: {e}")


        return conn