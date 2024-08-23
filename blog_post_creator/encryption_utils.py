from cryptography.fernet import Fernet
import base64

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.encode('utf-8').ljust(32)[:32])

def encrypt_token(token: str, password: str) -> str:
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted_token = fernet.encrypt(token.encode())
    return encrypted_token.decode()

def decrypt_token(encrypted_token: str, password: str) -> str:
    key = generate_key(password)
    fernet = Fernet(key)
    decrypted_token = fernet.decrypt(encrypted_token.encode())
    return decrypted_token.decode()
