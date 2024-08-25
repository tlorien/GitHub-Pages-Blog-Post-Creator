from cryptography.fernet import Fernet, InvalidToken
import base64
from blog_post_creator.blog_post_creator.utils.errors import EncryptionError
from blog_post_creator.utils.error_handler import handle_error

class EncryptionService:
    def __init__(self, key_generator=None):
        self.key_generator = key_generator or self.default_key_generator

    @staticmethod
    def default_key_generator(password: str) -> bytes:
        """Generates a key from the given password for encryption."""
        return base64.urlsafe_b64encode(password.encode('utf-8').ljust(32)[:32])

    def encrypt_token(self, token: str, password: str) -> str:
        """Encrypts the token using the given password."""
        try:
            key = self.key_generator(password)
            fernet = Fernet(key)
            encrypted_token = fernet.encrypt(token.encode())
            return encrypted_token.decode()
        except (TypeError, ValueError) as e:
            handle_error(e)
            raise EncryptionError(f"Failed to generate encryption key: {e}")
        except Exception as e:
            handle_error(e)
            raise EncryptionError(f"Failed to encrypt token: {e}")

    def decrypt_token(self, encrypted_token: str, password: str) -> str:
        """Decrypts the token using the given password."""
        try:
            key = self.key_generator(password)
            fernet = Fernet(key)
            decrypted_token = fernet.decrypt(encrypted_token.encode())
            return decrypted_token.decode()
        except InvalidToken as e:
            handle_error(e)
            raise EncryptionError("Invalid password or corrupted encrypted token.")
        except (TypeError, ValueError) as e:
            handle_error(e)
            raise EncryptionError(f"Failed to generate decryption key: {e}")
        except Exception as e:
            handle_error(e)
            raise EncryptionError(f"Failed to decrypt token: {e}")
