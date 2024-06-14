from typing import Optional

from DTO.LoginError import LoginError
from Models.User import User
from Repository.BaseClasses.DBRepository import DBRepository
from Service.HashService import HashService
from Service.IndexService import IndexService


class UserRepository:

    @staticmethod
    def find_by_credentials(username: str, password: str) -> (Optional[User], Optional[LoginError]):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        user_id = IndexService.find_user_by_username(username)

        if user_id is None:
            return None, LoginError.NotFound

        foundUser = cursor.execute(
            "SELECT id, username, password, role FROM user WHERE id = :user_id", {"user_id": user_id}
        )

        userValues = foundUser.fetchone()

        user = User(is_encrypted=True)
        user.populate(userValues, ['id', 'username', 'password', 'role'])
        user.decrypt()

        if HashService.verify_password(password, user.password):
            return user, ""

        return None, LoginError.BadCredentials
