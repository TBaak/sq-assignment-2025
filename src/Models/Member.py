from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class Member(EncryptableModel, DatabaseModel, SerializeableModel):
    ENCRYPTED_FIELDS = [
        'firstName',
        'lastName',
        'streetName',
        'age',
        'weight',
        'gender',
        'houseNumber',
        'city',
        'zipCode',
        'emailAddress',
        'phoneNumber',
        'number',
    ]

    # Member number
    number: str = None

    # Member information
    id: int = None
    firstName: str = None
    lastName: str = None
    age: str = None
    weight: str = None
    gender: str = None

    # Member contact details
    phoneNumber: str = None
    emailAddress: str = None

    # Member address
    streetName: str = None
    houseNumber: str = None
    zipCode: str = None
    city: str = None
