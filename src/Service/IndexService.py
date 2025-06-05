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

        IndexService.index[IndexDomain.SCOOTER_BRAND.name] = {}
        IndexService.index[IndexDomain.SCOOTER_MODEL.name] = {}
        IndexService.index[IndexDomain.SCOOTER_SERIAL_NUMBER.name] = {}
        IndexService.index[IndexDomain.SCOOTER_TOP_SPEED.name] = {}
        IndexService.index[IndexDomain.SCOOTER_STATE_OF_CHARGE.name] = {}
        IndexService.index[IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MIN.name] = {}
        IndexService.index[IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MAX.name] = {}
        IndexService.index[IndexDomain.SCOOTER_LOCATION_LAT.name] = {}
        IndexService.index[IndexDomain.SCOOTER_LOCATION_LNG.name] = {}
        IndexService.index[IndexDomain.SCOOTER_MILEAGE.name] = {}
        IndexService.index[IndexDomain.SCOOTER_LAST_MAINTENANCE_DATE.name] = {}
        IndexService.index[IndexDomain.SCOOTER_IN_SERVICE_DATE.name] = {}

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

        return results

    @staticmethod
    def find_scooter_by_query(query: str):
        results = []

        results = IndexService.__search_domain(IndexDomain.SCOOTER_BRAND, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_MODEL, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_SERIAL_NUMBER, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_TOP_SPEED, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_STATE_OF_CHARGE, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MIN, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MAX, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_LOCATION_LAT, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_LOCATION_LNG, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_MILEAGE, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_LAST_MAINTENANCE_DATE, query, results)
        results = IndexService.__search_domain(IndexDomain.SCOOTER_IN_SERVICE_DATE, query, results)


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
                       "phone_number "
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

    @staticmethod
    def __index_scooters():

        conn = DBRepository.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT "
                       "id, "
                       "brand, "
                       "model, "
                       "serial_number, "
                       "top_speed, "
                       "battery_capacity, "
                       "state_of_charge, "
                       "target_range_soc_min, "
                       "target_range_soc_max, "
                       "location_lat, "
                       "location_lng, "
                       "out_of_service_status, "
                       "mileage, "
                       "last_maintenance, "
                       "in_service_date "
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
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_TOP_SPEED,
                scooter[0],
                EncryptionService.decrypt(scooter[4])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_STATE_OF_CHARGE,
                scooter[0],
                EncryptionService.decrypt(scooter[5])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MIN,
                scooter[0],
                EncryptionService.decrypt(scooter[6])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_STATE_OF_CHARGE_TARGET_MAX,
                scooter[0],
                EncryptionService.decrypt(scooter[7])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_LOCATION_LAT,
                scooter[0],
                EncryptionService.decrypt(scooter[8])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_LOCATION_LNG,
                scooter[0],
                EncryptionService.decrypt(scooter[9])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_MILEAGE,
                scooter[0],
                EncryptionService.decrypt(scooter[10])
            )
            IndexService.__add_to_index(
                IndexDomain.SCOOTER_LAST_MAINTENANCE_DATE,
                scooter[0],
                EncryptionService.decrypt(scooter[11])
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
