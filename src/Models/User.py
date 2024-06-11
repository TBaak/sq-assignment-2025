from typing import Optional

from Models.DatabaseModel import DatabaseModel
from Models.EncryptableModel import EncryptableModel


class User(EncryptableModel, DatabaseModel):

    ENCRYPTED_FIELDS = ['username', 'password']

    id: Optional[int]
    username: str
    password: bytes
    role: str

