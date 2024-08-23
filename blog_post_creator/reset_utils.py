from blog_post_creator.utils import get_input
from blog_post_creator.config import handle_encrypted_token, set_env_variable_permanently
from blog_post_creator.encryption_utils import encrypt_token, decrypt_token
import os
import logging
import getpass

def reset_github_token():
    token = get_input("Enter a new GitHub token for the Blog Post Creator: ")
    password = getpass.getpass("Enter a password to encrypt your token: ")
    encrypted_token = encrypt_token(token, password)
    set_env_variable_permanently('BLOG_POST_CREATOR_GITHUB_TOKEN', encrypted_token)  # Set permanently
    os.environ['BLOG_POST_CREATOR_GITHUB_TOKEN'] = encrypted_token  # Temporarily store in environment to prevent issues with the active session
    logging.info("GitHub token has been reset and encrypted.")

def reset_password():
    encrypted_token = os.getenv('BLOG_POST_CREATOR_GITHUB_TOKEN')

    if not encrypted_token or encrypted_token == '1':
        print("No GitHub token found. Please reset the GitHub token first.")
        reset_github_token()
        return

    current_password = getpass.getpass("Enter the current password to decrypt the GitHub token: ")

    try:
        token = decrypt_token(encrypted_token, current_password)

        new_password = getpass.getpass("Enter a new password to encrypt your GitHub token: ")
        new_encrypted_token = encrypt_token(token, new_password)
        set_env_variable_permanently('BLOG_POST_CREATOR_GITHUB_TOKEN', new_encrypted_token)
        os.environ['BLOG_POST_CREATOR_GITHUB_TOKEN'] = new_encrypted_token
        logging.info("Password has been reset and token re-encrypted.")
    except Exception as e:
        logging.error("Incorrect password. Failed to decrypt the GitHub token.")
        print("Incorrect password. Please try again.")
        reset_password()
