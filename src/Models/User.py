from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class User(EncryptableModel, DatabaseModel, SerializeableModel):

    ENCRYPTED_FIELDS = ['username', 'password']

    id: int
    username: str
    password: bytes
    role: str


