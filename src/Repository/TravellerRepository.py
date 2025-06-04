import random
from datetime import datetime

from Models.Traveller import Traveller
from Repository.BaseClasses.DBRepository import DBRepository
from Service.IndexService import IndexService


class TravellerRepository:

    @staticmethod
    def find_all(ids: list[int] = None) -> list[Traveller]:
        db = DBRepository.create_connection()
        cursor = db.cursor()

        if ids is not None:
            cursor.execute('SELECT * FROM travellers WHERE id IN (%s)' % ','.join('?' * len(ids)), ids)
        else:
            cursor.execute("SELECT * FROM travellers")

        result = cursor.fetchall()

        cursor.close()
        db.close()

        travellers = []

        for travellerData in result:
            traveller = Traveller(is_encrypted=True)
            traveller.populate(travellerData, ['id', 'first_name', 'last_name', 'street_name', 'dob',  'gender',
                                         'house_number', 'city', 'zip_code', 'email_address', 'phone_number', 'number', 'driving_license_number'])
            traveller.decrypt()
            travellers.append(traveller)

        return travellers

    @staticmethod
    def find_by_query(query: str):
        if query == "":
            return TravellerRepository.find_all()

        traveller_ids = IndexService.find_traveller_by_query(query)

        if len(traveller_ids) == 0:
            return []

        return TravellerRepository.find_all(traveller_ids)



    @staticmethod
    def persist_traveller(traveller: Traveller):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        traveller.number = TravellerRepository.generate_traveller_number()

        traveller.encrypt()

        cursor.execute(
            "INSERT INTO travellers ("
            "first_name,"
            "last_name,"
            "dob,"
            "gender,"
            "street_name,"
            "house_number,"
            "city,"
            "zip_code,"
            "email_address,"
            "phone_number,"
            "number,"
            "driving_license_number"
            ") VALUES ("
            ":first_name,"
            ":last_name,"
            ":dob,"
            ":gender,"
            ":street_name,"
            ":house_number,"
            ":city,"
            ":zip_code,"
            ":email_address,"
            ":phone_number,"
            ":number,"
            ":driving_license_number"
            ");",
            traveller.serialize()
        )


        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def update_traveller(traveller):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        traveller.encrypt()

        cursor.execute(
            "UPDATE travellers SET "
            "first_name = :first_name,"
            "last_name = :last_name,"
            "dob = :dob,"
            "gender = :gender,"
            "street_name = :street_name,"
            "house_number = :house_number,"
            "city = :city,"
            "zip_code = :zip_code,"
            "email_address = :email_address,"
            "phone_number = :phone_number,"
            "driving_license_number = :driving_license_number "
            "WHERE id = :id",
            traveller.serialize()
        )


        db.commit()

        traveller.decrypt()

        cursor.close()
        db.close()

    @staticmethod
    def delete_traveller(traveller):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM travellers WHERE id = :id",
            traveller.serialize()
        )


        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def generate_traveller_number():
        # TODO: Check requirements
        year_last_two_digits = str(datetime.now().year)[2:]

        random_number = str(random.randint(1000000, 9999999))

        numbers = (year_last_two_digits + random_number)

        check_digit = sum(map(lambda x: int(x), [*numbers])) % 10

        return numbers + str(check_digit)