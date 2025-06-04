from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class Traveller(EncryptableModel, DatabaseModel, SerializeableModel):
    ENCRYPTED_FIELDS = [
        'first_name',
        'last_name',
        'street_name',
        'dob',
        'gender',
        'house_number',
        'city',
        'zip_code',
        'email_address',
        'phone_number',
        'number',
        'driving_license_number',
    ]

    # Traveller number
    number: str = None

    # Traveller information
    id: int = None
    first_name: str = None
    last_name: str = None
    dob: str = None
    gender: str = None
    driving_license_number: str = None

    # Traveller contact details
    phone_number: str = None
    email_address: str = None

    # Traveller address
    street_name: str = None
    house_number: str = None
    zip_code: str = None
    city: str = None
