from typing import Optional

from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel
from Models.User import User
from Repository.UserRepository import UserRepository


class BackupOneTimeCode(EncryptableModel, DatabaseModel, SerializeableModel):
    ENCRYPTED_FIELDS = ['one_time_code', 'backup_name']

    id: int = None
    user_id: int = None
    one_time_code: str = None
    backup_name: str = None

    def getUser(self) -> Optional['User']:
        return UserRepository.find_by_id(self.user_id)
