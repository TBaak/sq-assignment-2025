from Repository.BaseClasses.DBRepository import DBRepository
from Security.Enum.Role import Role
from Service.EncryptionService import EncryptionService
from Service.HashService import HashService


class CreateSystemAdminTest:

    @staticmethod
    def run(uname: str, pword: str):
        a = EncryptionService.encrypt(uname)
        b = EncryptionService.encrypt(HashService.hash(pword).decode())
        c = EncryptionService.encrypt(Role.SYSTEM_ADMIN.name)

        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", (a, b, c))

        db.commit()
        db.close()