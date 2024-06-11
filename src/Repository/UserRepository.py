from typing import Optional

from Models.User import User
from Repository.Repository import Repository
from Service.EncryptionService import EncryptionService
from Service.HashService import HashService
from Service.IndexService import IndexService


class UserRepository:

    @staticmethod
    def find_by_credentials(username: str, password: str) -> Optional[User]:
        db = Repository.create_connection()
        cursor = db.cursor()

        user_id = IndexService.find_user_by_username(username)

        if user_id is None:
            return None

        foundUser = cursor.execute(
            "SELECT id, username, password FROM user WHERE id = :user_id", {"user_id": user_id}
        )

        userValues = foundUser.fetchone()

        user = User(is_encrypted=True)
        user.populate(userValues, ['id', 'username', 'password'])
        user.decrypt()

        if HashService.verify_password(password, user.password):
            return user

        return None
