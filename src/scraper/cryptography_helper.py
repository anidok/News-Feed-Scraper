from cryptography.fernet import Fernet

KEY_PATH = 'keys/key.key'

class CryptographyHelper:
    @classmethod
    def decrypt(cls, encrypted):
        if encrypted is None:
            return None

        key = cls.get_key()
        encrypted_bytes = encrypted.encode()

        f = Fernet(key)
        decrypted_bytes = f.decrypt(encrypted_bytes)
        decrypted = decrypted_bytes.decode('utf-8')

        return decrypted

    @staticmethod
    def get_key():
        with open(KEY_PATH, 'rb') as file:
            key = file.read()

        return key
