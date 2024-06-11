import os
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509.oid import NameOID


class EncryptionService:
    PRIVATE_KEY_PATH = "private_key.pem"
    PUBLIC_KEY_PATH = "public_key.pem"

    @staticmethod
    def encrypt(data) -> bytes:
        cert = x509.load_pem_x509_certificate(EncryptionService.__get_encrypt_key())
        key = cert.public_key()
        encryptedData = key.encrypt(data.encode(), padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        return encryptedData

    @staticmethod
    def decrypt(data) -> str:
        key = load_pem_private_key(EncryptionService.__get_decrypt_key(), password=b"super_admin")
        decryptedData = key.decrypt(data, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        return decryptedData.decode()

    @staticmethod
    def __get_encrypt_key() -> bytes:
        with open(EncryptionService.PUBLIC_KEY_PATH, 'rb') as f:
            key = f.read()
            return key

    @staticmethod
    def __get_decrypt_key() -> bytes:
        with open(EncryptionService.PRIVATE_KEY_PATH, 'rb') as f:
            key = f.read()
            return key
        pass

    @staticmethod
    def create_certificates_if_not_exist():
        publicExists = os.path.exists(EncryptionService.PUBLIC_KEY_PATH)
        privateExists = os.path.exists(EncryptionService.PRIVATE_KEY_PATH)

        if not publicExists or not privateExists:
            EncryptionService.create_certificates()

    @staticmethod
    def create_certificates():
        certKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        bytesKey = certKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"super_admin")
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "NL"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Zuid-Holland"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Rotterdam"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "WebSec"),
            x509.NameAttribute(NameOID.COMMON_NAME, "websec.example.com"),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            certKey.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.now()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.now() + timedelta(days=3650)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
            # Sign our certificate with our private key
        ).sign(certKey, hashes.SHA256())

        with open(EncryptionService.PUBLIC_KEY_PATH, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        with open(EncryptionService.PRIVATE_KEY_PATH, "wb") as f:
            f.write(bytesKey)
