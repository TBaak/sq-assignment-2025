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
