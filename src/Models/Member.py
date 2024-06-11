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
        'phoneNumber'
    ]

    # Member information
    id: int
    firstName: str
    lastName: str
    age: str
    weight: str
    gender: str

    # Member contact details
    phoneNumber: str
    emailAddress: str

    # Member address
    streetName: str
    houseNumber: str
    zipCode: str
    city: str
