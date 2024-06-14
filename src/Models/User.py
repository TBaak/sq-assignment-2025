from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class User(EncryptableModel, DatabaseModel, SerializeableModel):

    ENCRYPTED_FIELDS = ['username', 'password', 'role']

    id: int = None
    username: str = None
    password: bytes = None
    role: str = None


