from enum import Enum


class IndexDomain(Enum):
    USER_ROLE = "user_role"
    USER_USERNAME = "user_username"
    USER_FIRSTNAME = "user_firstname"
    USER_LASTNAME = "user_lastname"

    MEMBER_NUMBER = "member_number"
    MEMBER_FIRSTNAME = "member_firstname"
    MEMBER_LASTNAME = "member_lastname"
    MEMBER_ADDRESS = "member_address"
    MEMBER_EMAIL = "member_email"
    MEMBER_PHONE = "member_phone"
