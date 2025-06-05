from enum import Enum


class IndexDomain(Enum):
    USER_ROLE = "user_role"
    USER_USERNAME = "user_username"
    USER_FIRSTNAME = "user_firstname"
    USER_LASTNAME = "user_lastname"

    TRAVELLER_NUMBER = "traveller_number"
    TRAVELLER_FIRSTNAME = "traveller_firstname"
    TRAVELLER_LASTNAME = "traveller_lastname"
    TRAVELLER_ADDRESS = "traveller_address"
    TRAVELLER_EMAIL = "traveller_email"
    TRAVELLER_PHONE = "traveller_phone"

    SCOOTER_BRAND = "scooter_brand"
    SCOOTER_MODEL = "scooter_model"
    SCOOTER_SERIAL_NUMBER = "scooter_serial_number"
    SCOOTER_TOP_SPEED = "scooter_top_speed"
    SCOOTER_STATE_OF_CHARGE = "scooter_state_of_charge"
    SCOOTER_STATE_OF_CHARGE_TARGET_MIN = "scooter_state_of_charge_target_min"
    SCOOTER_STATE_OF_CHARGE_TARGET_MAX = "scooter_state_of_charge_target_max"
    SCOOTER_LOCATION_LAT = "scooter_location_lat"
    SCOOTER_LOCATION_LNG = "scooter_location_lng"
    SCOOTER_MILEAGE = "scooter_mileage"
    SCOOTER_LAST_MAINTENANCE_DATE = "scooter_last_maintenance_date"
    SCOOTER_IN_SERVICE_DATE = "scooter_in_service_date"
