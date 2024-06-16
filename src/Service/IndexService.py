from typing import Optional

from Debug.ConsoleLogger import ConsoleLogger
from Enum.IndexDomain import IndexDomain
from Models.User import User
from Repository.BaseClasses.DBRepository import DBRepository
from Security.Enum.Role import Role
from Service.EncryptionService import EncryptionService


class IndexService:
    index: object = None

    @staticmethod
    def index_database():
        ConsoleLogger.v("Indexing database")

        IndexService.index = {}

        IndexService.__init_domains()

        IndexService.__index_users()
        IndexService.__index_members()

        ConsoleLogger.v("Database indexed")

        pass

    @staticmethod
    def __init_domains():
        IndexService.index[IndexDomain.USER_USERNAME.value] = {}
        IndexService.index[IndexDomain.USER_ROLE.value] = {}
        IndexService.index[IndexDomain.USER_FIRSTNAME.value] = {}
        IndexService.index[IndexDomain.USER_LASTNAME.value] = {}
        IndexService.index[IndexDomain.MEMBER_NUMBER.value] = {}
        IndexService.index[IndexDomain.MEMBER_FIRSTNAME.value] = {}
        IndexService.index[IndexDomain.MEMBER_LASTNAME.value] = {}
        IndexService.index[IndexDomain.MEMBER_ADDRESS.value] = {}
        IndexService.index[IndexDomain.MEMBER_EMAIL.value] = {}
        IndexService.index[IndexDomain.MEMBER_PHONE.value] = {}

    @staticmethod
    def add_user_to_index(user: User):
        pass

    @staticmethod
    def find_user_by_username(username: str) -> Optional[int]:
        for key, value in IndexService.index[IndexDomain.USER_USERNAME.value].items():
            if key == username:
                return value[0]

    @staticmethod
    def find_member_by_query(query: str):
        results = []

        results = IndexService.__search_domain(IndexDomain.MEMBER_NUMBER, query, results)
        results = IndexService.__search_domain(IndexDomain.MEMBER_FIRSTNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.MEMBER_LASTNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.MEMBER_ADDRESS, query, results)
        results = IndexService.__search_domain(IndexDomain.MEMBER_EMAIL, query, results)
        results = IndexService.__search_domain(IndexDomain.MEMBER_PHONE, query, results)

        return results

    @staticmethod
    def find_user_by_query(query, role: Role):

        resultsForRole = IndexService.find_user_by_role(role)

        results = []

        results = IndexService.__search_domain(IndexDomain.USER_USERNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.USER_FIRSTNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.USER_LASTNAME, query, results)

        return IndexService.__intersection(results, resultsForRole)

    @staticmethod
    def find_user_by_role(role: Role):
        return IndexService.__search_domain(IndexDomain.USER_ROLE, role.name.lower(), [])

    @staticmethod
    def __search_domain(domain: IndexDomain, query: str, results: list[int]):
        for key, value in IndexService.index[domain.value].items():
            if query in key:
                results = results + value
        return results

    @staticmethod
    def __index_users():

        ConsoleLogger.v("Indexing users")

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, role, firstName, lastName FROM user")
        users = cursor.fetchall()

        for user in users:
            IndexService.__add_to_index(
                IndexDomain.USER_USERNAME,
                user[0],
                EncryptionService.decrypt(user[1])
            )
            IndexService.__add_to_index(
                IndexDomain.USER_ROLE,
                user[0],
                EncryptionService.decrypt(user[2])
            )
            IndexService.__add_to_index(
                IndexDomain.USER_FIRSTNAME,
                user[0],
                EncryptionService.decrypt(user[3])
            )
            IndexService.__add_to_index(
                IndexDomain.USER_LASTNAME,
                user[0],
                EncryptionService.decrypt(user[4])
            )

        ConsoleLogger.v("Users indexed")

    @staticmethod
    def __index_members():

        ConsoleLogger.v("Indexing Members")

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT "
                       "id,"
                       "number,"
                       "firstName,"
                       "lastName,"

                       "streetName,"
                       "houseNumber,"
                       "zipCode,"

                       "emailAddress,"
                       "phoneNumber "
                       "FROM member")
        users = cursor.fetchall()

        for user in users:
            IndexService.__add_to_index(
                IndexDomain.MEMBER_NUMBER,
                user[0],
                EncryptionService.decrypt(user[1])
            )
            IndexService.__add_to_index(
                IndexDomain.MEMBER_FIRSTNAME,
                user[0],
                EncryptionService.decrypt(user[2])
            )
            IndexService.__add_to_index(
                IndexDomain.MEMBER_LASTNAME,
                user[0],
                EncryptionService.decrypt(user[3])
            )
            IndexService.__add_to_index(
                IndexDomain.MEMBER_ADDRESS,
                user[0],
                EncryptionService.decrypt(user[4]) + " "
                + EncryptionService.decrypt(user[5]) + " "
                + EncryptionService.decrypt(user[6])
            )
            IndexService.__add_to_index(
                IndexDomain.MEMBER_EMAIL,
                user[0],
                EncryptionService.decrypt(user[7])
            )
            IndexService.__add_to_index(
                IndexDomain.MEMBER_PHONE,
                user[0],
                EncryptionService.decrypt(user[8])
            )

        ConsoleLogger.v("Members indexed")

    @staticmethod
    def __add_to_index(domain: IndexDomain, database_id: int, value: str):

        if IndexService.index is None:
            IndexService.index = {}

        if domain.value not in IndexService.index:
            IndexService.index[domain.value] = {}

        if value.lower() not in IndexService.index[domain.value]:
            IndexService.index[domain.value][value.lower()] = []

        IndexService.index[domain.value][value.lower()].append(database_id)

    @staticmethod
    def __intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3