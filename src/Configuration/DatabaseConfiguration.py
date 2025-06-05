import os
from sqlite3 import Connection

from Repository.BaseClasses.DBRepository import DBRepository


class DatabaseConfiguration:
    db_connection = None

    @staticmethod
    def start():
        db = DBRepository.create_connection()

        DatabaseConfiguration.__table_travellers(db)
        DatabaseConfiguration.__table_users(db)
        DatabaseConfiguration.__table_scooters(db)

        db.close()

    @staticmethod
    def __table_travellers(db: Connection):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateTravellerTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()


        db.commit()

    @staticmethod
    def __table_users(db: Connection):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateUserTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()


        db.commit()

    @staticmethod
    def __table_scooters(db: Connection):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateScooterTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()


        db.commit()
