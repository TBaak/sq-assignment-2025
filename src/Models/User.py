from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class User(EncryptableModel, DatabaseModel, SerializeableModel):
    ENCRYPTED_FIELDS = ['username', 'password', 'role', 'first_name', 'last_name', 'registration_date']

    id: int = None
    username: str = None
    password: str = None
    role: str = None
    first_name: str = None
    last_name: str = None
    registration_date: str = None  # String because this works easier with encryption
