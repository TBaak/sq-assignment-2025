import os
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509.oid import NameOID

from Enum.Color import Color
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


class EncryptionService:

    key_filename = "fernet.key"
    key_dir = "../../Storage"

    @staticmethod
    def encrypt(data: str) -> str:
        f = EncryptionService.__create_fernet()
        token = f.encrypt(data.encode())
        return token.decode()

    @staticmethod
    def decrypt(data: str) -> str:
        f = EncryptionService.__create_fernet()
        plain = f.decrypt(data.encode())
        return plain.decode()

    @staticmethod
    def __create_fernet() -> Fernet:
        base_dir = os.path.dirname(os.path.realpath(__file__))

        if not os.path.exists(os.path.realpath(base_dir + EncryptionService.key_dir)):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Encryptie opslag fout, afsluiten...", Color.FAIL),
                1
            )
            exit(1)

        key_path = os.path.realpath(base_dir + EncryptionService.key_dir + "/" + EncryptionService.key_filename);

        if not os.path.exists(key_path):
            key = Fernet.generate_key()

            with open(key_path, 'w') as file:
                file.write(key.decode())

            return Fernet(key)

        with open(key_path, 'rb') as f:
            key = f.read()
            return Fernet(key)



