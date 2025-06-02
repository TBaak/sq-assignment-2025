import os
from sqlite3 import Connection

from Debug.ConsoleLogger import ConsoleLogger
from Repository.BaseClasses.DBRepository import DBRepository


class DatabaseConfiguration:
    dbConnection = None

    @staticmethod
    def start():
        db = DBRepository.create_connection()

        DatabaseConfiguration.__table_traveller(db)
        DatabaseConfiguration.__table_user(db)

        db.close()

    @staticmethod
    def __table_traveller(db: Connection):

        ConsoleLogger.v("Creating traveller table if not exist")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateTravellerTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()

        ConsoleLogger.v("Traveller table created")

        db.commit()

    @staticmethod
    def __table_user(db: Connection):

        ConsoleLogger.v("Creating user table if not exist")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateUserTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()

        ConsoleLogger.v("User table created")

        db.commit()
