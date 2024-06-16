import string
import random
from typing import Optional

from DTO.LoginError import LoginError
from Debug.ConsoleLogger import ConsoleLogger
from Enum.UserType import UserType
from Models.User import User
from Repository.BaseClasses.DBRepository import DBRepository
from Security.Enum.Role import Role
from Service.HashService import HashService
from Service.IndexService import IndexService


class UserRepository:

    @staticmethod
    def find_all_by_role(role: Role, ids: list[int] = None) -> list[User]:
        db = DBRepository.create_connection()
        cursor = db.cursor()

        if ids is None:
            ids = IndexService.find_user_by_role(role)

        cursor.execute('SELECT id, username, password, role, firstName, lastName, registrationDate FROM user '
                       'WHERE id IN (%s)' % ','.join('?' * len(ids)), ids)

        result = cursor.fetchall()

        cursor.close()
        db.close()

        users = []

        for userData in result:
            user = User(is_encrypted=True)
            user.populate(userData, ['id', 'username', 'password', 'role', 'firstName', 'lastName', 'registrationDate'])
            user.decrypt()
            users.append(user)

        return users

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

    @staticmethod
    def persist_user(user):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        user.encrypt()

        cursor.execute(
            "INSERT INTO user ("
            "firstName,"
            "lastName,"
            "role,"
            "username,"
            "password,"
            "registrationDate"
            ") VALUES ("
            ":firstName,"
            ":lastName,"
            ":role,"
            ":username,"
            ":password,"
            ":registrationDate"
            ");",
            user.serialize()
        )

        ConsoleLogger.vv("User member: " + str(user.serialize()))

        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def update_user(user):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        user.encrypt()

        cursor.execute(
            "UPDATE user SET "
            "firstName = :firstName,"
            "lastName = :lastName,"
            "username = :username "
            "WHERE id = :id",
            user.serialize()
        )

        ConsoleLogger.vv("Updated user: " + str(user.serialize()))

        db.commit()

        user.decrypt()

        cursor.close()
        db.close()

    @staticmethod
    def update_user_password(user):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        user.encrypt()

        cursor.execute(
            "UPDATE user SET "
            "password = :password "
            "WHERE id = :id",
            user.serialize()
        )

        ConsoleLogger.vv("Updated user password: " + str(user.serialize()))

        db.commit()

        user.decrypt()

        cursor.close()
        db.close()

    @staticmethod
    def generate_valid_password() -> str:
        # Define the character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_characters = "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/"

        # Ensure the password contains at least one of each required character type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_characters)
        ]
        
        # Fill the rest of the password length with random choices from all allowed characters
        all_characters = lowercase + uppercase + digits + special_characters
        password_length = random.randint(12, 30)
        password += random.choices(all_characters, k=password_length - 4)

        # Shuffle the resulting password list to avoid predictable sequences
        random.shuffle(password)

        # Convert the list to a string and return
        return ''.join(password)

    @staticmethod
    def delete_user(user: User):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM member WHERE id = :id",
            user.serialize()
        )

        ConsoleLogger.vv("Deleted member: " + str(user.id))

        db.commit()

        cursor.close()
        db.close()