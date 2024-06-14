from Repository.BaseClasses.DBRepository import DBRepository
from Security.Enum.Role import Role
from Service.EncryptionService import EncryptionService
from Service.HashService import HashService


class CreateConsultantTest:

    @staticmethod
    def run(uname: str, pword: str):
        a = EncryptionService.encrypt(uname)
        b = EncryptionService.encrypt(HashService.hash(pword).decode())
        c = EncryptionService.encrypt(Role.CONSULTANT.name)

        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", (a, b, c))

        db.commit()
        db.close()