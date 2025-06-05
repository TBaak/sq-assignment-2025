import random
from datetime import datetime

from Models.Scooter import Scooter
from Models.Traveller import Traveller
from Repository.BaseClasses.DBRepository import DBRepository
from Security.AuthorizationDecorator import Auth
from Security.AuthorizationService import AuthorizationService
from Security.Enum.Permission import Permission
from Service.IndexService import IndexService


class ScooterRepository:

    @staticmethod
    def find_all(ids: list[int] = None) -> list[Scooter]:
        db = DBRepository.create_connection()
        cursor = db.cursor()

        if ids is not None:
            cursor.execute('SELECT * FROM scooters WHERE id IN (%s)' % ','.join('?' * len(ids)), ids)
        else:
            cursor.execute("SELECT * FROM scooters")

        result = cursor.fetchall()

        cursor.close()
        db.close()

        scooters = []

        for scooterData in result:
            scooter = Scooter(is_encrypted=True)
            scooter.populate(scooterData,
                               [
                                   'id',
                                   'brand',
                                   'model',
                                   'serial_number',
                                   'top_speed',
                                   'battery_capacity',
                                   'state_of_charge',
                                   'target_range_soc_min',
                                   'target_range_soc_max',
                                   'location_lat',
                                   'location_lng',
                                   'out_of_service_status',
                                   'mileage',
                                   'last_maintenance',
                                   'in_service_date'
                                ])
            scooter.decrypt()
            scooters.append(scooter)

        return scooters

    @staticmethod
    def find_by_query(query: str):
        if query == "":
            return ScooterRepository.find_all()

        scooter_ids = IndexService.find_scooter_by_query(query)

        if len(scooter_ids) == 0:
            return []

        return ScooterRepository.find_all(scooter_ids)



    @staticmethod
    def persist_scooter(scooter: Scooter):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        scooter.encrypt()

        cursor.execute(
            "INSERT INTO scooters ("
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
            "in_service_date"
            ") VALUES ("
            ":brand, "
            ":model, "
            ":serial_number, "
            ":top_speed, "
            ":battery_capacity, "
            ":state_of_charge, "
            ":target_range_soc_min, "
            ":target_range_soc_max, "
            ":location_lat, "
            ":location_lng, "
            ":out_of_service_status, "
            ":mileage, "
            ":last_maintenance, "
            ":in_service_date"
            ");",
            scooter.serialize()
        )


        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    @Auth.permission_required(Permission.ScooterUpdateFull)
    def update_scooter_full(scooter: Scooter):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        scooter.encrypt()

        cursor.execute(
            "UPDATE scooters SET "
            "brand = :brand, "
            "model = :model, "
            "serial_number = :serial_number, "
            "top_speed = :top_speed, "
            "battery_capacity = :battery_capacity, "
            "state_of_charge = :state_of_charge, "
            "target_range_soc_min = :target_range_soc_min, "
            "target_range_soc_max = :target_range_soc_max, "
            "location_lat = :location_lat, "
            "location_lng = :location_lng, "
            "out_of_service_status = :out_of_service_status, "
            "mileage = :mileage, "
            "last_maintenance = :last_maintenance "
            "WHERE id = :id",
            scooter.serialize()
        )

        db.commit()

        scooter.decrypt()

        cursor.close()
        db.close()

    @staticmethod
    @Auth.permission_required(Permission.ScooterUpdatePartial)
    def update_scooter_partial(scooter: Scooter):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        scooter.encrypt()

        cursor.execute(
            "UPDATE scooters SET "
            "state_of_charge = :state_of_charge, "
            "target_range_soc_min = :target_range_soc_min, "
            "target_range_soc_max = :target_range_soc_max, "
            "location_lat = :location_lat, "
            "location_lng = :location_lng, "
            "out_of_service_status = :out_of_service_status, "
            "mileage = :mileage, "
            "last_maintenance = :last_maintenance "
            "WHERE id = :id",
            scooter.serialize()
        )

        db.commit()

        scooter.decrypt()

        cursor.close()
        db.close()

    @staticmethod
    def delete_traveller(traveller):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM scooters WHERE id = :id",
            traveller.serialize()
        )


        db.commit()

        cursor.close()
        db.close()