from Enum.IndexDomain import IndexDomain
from Models.User import User
from Repository.Repository import Repository
from Service.EncryptionService import EncryptionService


class IndexService:
    index: object = None

    @staticmethod
    def index_database():
        IndexService.__index_users()
        pass

    @staticmethod
    def add_user_to_index(user: User):
        pass

    @staticmethod
    def find_user_by_username(username: str) -> int:
        for key, value in IndexService.index[IndexDomain.USER_USERNAME].items():
            if key == username:
                return value[0]

    @staticmethod
    def __index_users():
        conn = Repository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username FROM user")
        users = cursor.fetchall()

        for user in users:
            IndexService.__add_to_index(
                IndexDomain.USER_USERNAME,
                user[0],
                EncryptionService.decrypt(user[1])
            )

    @staticmethod
    def __add_to_index(domain: IndexDomain, database_id: int, value: str):

        if IndexService.index is None:
            IndexService.index = {}

        if domain not in IndexService.index:
            IndexService.index[domain] = {}

        if value not in IndexService.index[domain]:
            IndexService.index[domain][value] = []

        IndexService.index[domain][value].append(database_id)
