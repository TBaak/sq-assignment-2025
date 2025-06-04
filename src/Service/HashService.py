import bcrypt


class HashService:

    # TODO: Add manual salt as described in the lessons

    @staticmethod
    def hash(input: str) -> bytes:
        inputBytes = input.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(inputBytes, salt)

        return hashed

    @staticmethod
    def verify_password(a, b):
        return bcrypt.checkpw(a.encode(), b.encode())
