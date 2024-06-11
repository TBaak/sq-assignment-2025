from Repository.Repository import Repository
from Service.EncryptionService import EncryptionService
from Service.HashService import HashService


class CreateAdminTest:

    @staticmethod
    def run(uname: str, pword: str):
        a = EncryptionService.encrypt(uname)
        b = EncryptionService.encrypt(HashService.hash(pword).decode())

        db = Repository.create_connection()
        cursor = db.cursor()

        cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, 'test')", (a, b))

        db.commit()
        db.close()