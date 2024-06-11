from Service.EncryptionService import EncryptionService


class EncryptableModel:
    ENCRYPTED_FIELDS = []

    is_encrypted = False

    def __init__(self, is_encrypted: bool = False):
        self.is_encrypted = is_encrypted

    def encrypt(self):
        if self.is_encrypted:
            return
        self.is_encrypted = True
        for field in self.ENCRYPTED_FIELDS:
            value = getattr(self, field)
            setattr(self, field, EncryptionService.encrypt(value))

    def decrypt(self):
        if not self.is_encrypted:
            return
        self.is_encrypted = False
        for field in self.ENCRYPTED_FIELDS:
            value = getattr(self, field)
            setattr(self, field, EncryptionService.decrypt(value))
