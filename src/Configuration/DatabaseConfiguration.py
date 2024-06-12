import os
from sqlite3 import Connection

from Debug.ConsoleLogger import ConsoleLogger
from Repository.Repository import Repository


class DatabaseConfiguration:
    dbConnection = None

    @staticmethod
    def start():

        # TODO: Handle database errors

        db = Repository.create_connection()

        DatabaseConfiguration.__table_member(db)
        DatabaseConfiguration.__table_user(db)

        db.close()

    @staticmethod
    def __table_member(db: Connection):

        ConsoleLogger.v("Creating member table if not exist")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/DatabaseScripts/CreateMemberTable.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        cursor.close()

        ConsoleLogger.v("Member table created")

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
