from typing import Optional

from Enum.IndexDomain import IndexDomain
from Models.User import User
from Repository.BaseClasses.DBRepository import DBRepository
from Security.Enum.Role import Role
from Service.EncryptionService import EncryptionService


class IndexService:
    index: object = None

    @staticmethod
    def index_database():

        IndexService.index = {}

        IndexService.__init_domains()

        IndexService.__index_users()
        IndexService.__index_travellers()
        IndexService.__index_scooters()

        pass

    @staticmethod
    def __init_domains():
        IndexService.index[IndexDomain.USER_USERNAME.value] = {}
        IndexService.index[IndexDomain.USER_ROLE.value] = {}
        IndexService.index[IndexDomain.USER_FIRSTNAME.value] = {}
        IndexService.index[IndexDomain.USER_LASTNAME.value] = {}

        IndexService.index[IndexDomain.TRAVELLER_NUMBER.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_FIRSTNAME.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_LASTNAME.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_ADDRESS.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_EMAIL.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_PHONE.value] = {}
        IndexService.index[IndexDomain.TRAVELLER_DRIVING_LICENSE_NUMBER.value] = {}

        IndexService.index[IndexDomain.SCOOTER_BRAND.value] = {}
        IndexService.index[IndexDomain.SCOOTER_MODEL.value] = {}
        IndexService.index[IndexDomain.SCOOTER_SERIAL_NUMBER.value] = {}

    @staticmethod
    def add_user_to_index(user: User):
        pass

    @staticmethod
    def find_user_by_username(username: str) -> Optional[int]:
        for key, value in IndexService.index[IndexDomain.USER_USERNAME.value].items():
            if key == username:
                return value[0]

    @staticmethod
    def find_traveller_by_query(query: str):
        results = []

        results = IndexService.__search_domain(IndexDomain.TRAVELLER_NUMBER, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_FIRSTNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_LASTNAME, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_ADDRESS, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_EMAIL, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_PHONE, query, results)
        results = IndexService.__search_domain(IndexDomain.TRAVELLER_DRIVING_LICENSE_NUMBER, query, results)

        return results

    @staticmethod
    def find_scooter_by_query(query: str):
        results = []

        results = IndexService.__search_domain(IndexDomain.SCOOTER_BRAND, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_MODEL, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_SERIAL_NUMBER, query, results)

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

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, role, first_name, last_name FROM users")
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

    @staticmethod
    def __index_travellers():

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT "
                       "id,"
                       "number,"
                       "first_name,"
                       "last_name,"

                       "street_name,"
                       "house_number,"
                       "zip_code,"

                       "email_address,"
                       "phone_number, "
                       "driving_license_number "
                       "FROM travellers")
        users = cursor.fetchall()

        for user in users:
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_NUMBER,
                user[0],
                EncryptionService.decrypt(user[1])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_FIRSTNAME,
                user[0],
                EncryptionService.decrypt(user[2])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_LASTNAME,
                user[0],
                EncryptionService.decrypt(user[3])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_ADDRESS,
                user[0],
                EncryptionService.decrypt(user[4]) + " "
                + EncryptionService.decrypt(user[5]) + " "
                + EncryptionService.decrypt(user[6])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_EMAIL,
                user[0],
                EncryptionService.decrypt(user[7])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_PHONE,
                user[0],
                EncryptionService.decrypt(user[8])
            )
            IndexService.__add_to_index(
                IndexDomain.TRAVELLER_DRIVING_LICENSE_NUMBER,
                user[0],
                EncryptionService.decrypt(user[9])
            )

    @staticmethod
    def __index_scooters():

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT "
                       "id, "
                       "brand, "
                       "model, "
                       "serial_number "
                       "FROM scooters")
        scooters = cursor.fetchall()

        for scooter in scooters:
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_BRAND,
                scooter[0],
                EncryptionService.decrypt(scooter[1])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_MODEL,
                scooter[0],
                EncryptionService.decrypt(scooter[2])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_SERIAL_NUMBER,
                scooter[0],
                EncryptionService.decrypt(scooter[3])
            )



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
