import bcrypt


class HashService:

    @staticmethod
    def hash(plain: str) -> str:
        input_bytes = plain.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(input_bytes, salt)

        return hashed.decode()

    @staticmethod
    def verify_password(a, b):
        return bcrypt.checkpw(a.encode(), b.encode())
