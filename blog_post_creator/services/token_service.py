import os
import logging
import platform
from blog_post_creator.blog_post_creator.utils.errors import ConfigError, EncryptionError
from blog_post_creator.services.encryption_service import EncryptionService
from blog_post_creator.utils.error_handler import handle_error
from blog_post_creator.infrastructure.input_handler import InputHandler

class TokenService:
    def __init__(self, encryption_service: EncryptionService, input_handler: InputHandler):
        self.encryption_service = encryption_service
        self.input_handler = input_handler
        self.env_var_name = 'BLOG_POST_CREATOR_GITHUB_TOKEN'
        self._decrypted_token = None

    def get_encrypted_token(self):
        """Retrieve the encrypted GitHub token from environment variables."""
        encrypted_token = os.getenv(self.env_var_name)
        if not encrypted_token or encrypted_token == '1':
            logging.info("GitHub token is missing or invalid.")
            return None
        return encrypted_token

    def decrypt_token_once(self):
        """Decrypt the GitHub token only once for the duration of an operation."""
        if self._decrypted_token:
            return self._decrypted_token

        encrypted_token = self.get_encrypted_token()
        if not encrypted_token:
            raise ConfigError("No GitHub token found. Please set a token first.")

        password = self.input_handler.get_secure_input("Enter your password to decrypt the GitHub token: ")

        try:
            self._decrypted_token = self.encryption_service.decrypt_token(encrypted_token, password)
            return self._decrypted_token
        except EncryptionError as e:
            handle_error(e)
            self._decrypted_token = None
            raise

    def clear_decrypted_token(self):
        """Clear the decrypted token from memory."""
        self._decrypted_token = None

    def encrypt_and_store_token(self):
        """Encrypt the GitHub token with a password and store it securely."""
        token = self.input_handler.get_secure_input("Enter a new GitHub token for the Blog Post Creator: ")
        password = self.input_handler.get_secure_input("Enter a password to encrypt your token: ")

        try:
            encrypted_token = self.encryption_service.encrypt_token(token, password)
            self.update_env_variable(self.env_var_name, encrypted_token)
            logging.info("GitHub token has been reset and stored securely.")
        except EncryptionError as e:
            handle_error(e)
            raise

    def reset_password(self):
        """Reset the password used to encrypt the GitHub token."""
        encrypted_token = self.get_encrypted_token()
        if not encrypted_token:
            raise ConfigError("No GitHub token found. Please set a token first.")

        current_password = self.input_handler.get_secure_input("Enter the current password to decrypt the GitHub token: ")

        try:
            token = self.encryption_service.decrypt_token(encrypted_token, current_password)
        except EncryptionError as e:
            handle_error(e)
            print("Incorrect password. Please try again.")
            return

        new_password = self.input_handler.get_secure_input("Enter a new password to encrypt your GitHub token: ")

        try:
            new_encrypted_token = self.encryption_service.encrypt_token(token, new_password)
            self.update_env_variable(self.env_var_name, new_encrypted_token)
            self.clear_decrypted_token()
            logging.info("Password has been reset and token re-encrypted.")
        except EncryptionError as e:
            handle_error(e)
            raise

    def update_env_variable(self, name, value):
        """Update an environment variable both for the current session and permanently."""
        os.environ[name] = value

        system = platform.system()
        try:
            if system == 'Windows':
                os.system(f"setx {name} {value}")
                logging.info(f"Environment variable {name} set permanently on Windows.")
            elif system in ['Linux', 'Darwin']:
                shell_profile = os.path.expanduser("~/.bashrc")
                if os.path.exists(os.path.expanduser("~/.zshrc")):
                    shell_profile = os.path.expanduser("~/.zshrc")

                with open(shell_profile, "a") as file:
                    file.write(f'\nexport {name}="{value}"\n')
                logging.info(f"Environment variable {name} set permanently in {shell_profile}.")
            else:
                raise ConfigError(f"Unsupported operating system: {system}")
        except Exception as e:
            handle_error(e)
