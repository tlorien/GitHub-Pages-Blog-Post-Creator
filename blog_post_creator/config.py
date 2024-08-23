import os
import configparser
import logging
import platform
from blog_post_creator.utils import get_input
from blog_post_creator.encryption_utils import encrypt_token, decrypt_token
import subprocess
import getpass

def load_config(config_file="config/config.ini"):
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        logging.warning(f"Configuration file {config_file} not found. Creating a new one with default values.")
        create_default_config(config_file)

    config.read(config_file)

    config = prompt_for_missing_config(config, config_file)

    return config

def create_default_config(config_file):
    config = configparser.ConfigParser()
    config['github'] = {
        'repo_owner': '',
        'repo_name': '',
        'branch': 'main'
    }
    config['post'] = {
        'posts_dir': '_posts'
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)
    logging.info(f"Default configuration file created at {config_file}.")

def prompt_for_missing_config(config, config_file):
    if 'github' not in config:
        config['github'] = {}
    
    if 'post' not in config:
        config['post'] = {}

    if not config['github'].get('repo_owner'):
        config['github']['repo_owner'] = get_input("Enter the GitHub repository owner: ")
    if not config['github'].get('repo_name'):
        config['github']['repo_name'] = get_input("Enter the GitHub repository name: ")
    if not config['github'].get('branch'):
        config['github']['branch'] = get_input("Enter the branch to push to (default 'main'): ") or 'main'

    if not config['post'].get('posts_dir'):
        config['post']['posts_dir'] = get_input("Enter the directory for posts (default '_posts'): ") or '_posts'

    with open(config_file, 'w') as configfile:
        config.write(configfile)
    logging.info(f"Configuration updated and saved to {config_file}.")

    return config

def set_env_variable_permanently(name, value):
    system = platform.system()

    if system == 'Windows':
        subprocess.run(["setx", name, value], shell=True)
        logging.info(f"Environment variable {name} set permanently on Windows.")
    elif system in ['Linux', 'Darwin']:  # Darwin is macOS
        shell_profile = os.path.expanduser("~/.bashrc")  # Default to bashrc
        if os.path.exists(os.path.expanduser("~/.zshrc")):
            shell_profile = os.path.expanduser("~/.zshrc")  # Use zshrc if it exists

        with open(shell_profile, "a") as file:
            file.write(f'\nexport {name}="{value}"\n')
        logging.info(f"Environment variable {name} set permanently in {shell_profile}.")
    else:
        logging.error(f"Unsupported operating system: {system}")

def handle_encrypted_token(env_var_name, invalid_token=False):
    encrypted_token = os.getenv(env_var_name)
    logging.debug(f"Retrieved encrypted token from environment: {encrypted_token}")

    if invalid_token:
        token = get_input("Your GitHub token is invalid. Enter a new GitHub token for the Blog Post Creator: ")
        password = getpass.getpass("Enter a password to encrypt your token: ")
        encrypted_token = encrypt_token(token, password)
        set_env_variable_permanently(env_var_name, encrypted_token)  # Set permanently
        os.environ[env_var_name] = encrypted_token  # Temporarily store in environment for the session
        logging.info(f"Encrypted GitHub token stored in environment variable {env_var_name}.")
        return token

    if encrypted_token and encrypted_token != '1':
        password = getpass.getpass("Enter your password to decrypt the GitHub token: ")
        try:
            token = decrypt_token(encrypted_token, password)
            logging.debug(f"Decrypted token: {token}")
            return token
        except Exception as e:
            logging.error("Decryption failed. The password might be incorrect.")
            return handle_encrypted_token(env_var_name)

    token = get_input("Your GitHub token is invalid or not set. Enter a new GitHub token for the Blog Post Creator: ")
    password = getpass.getpass("Enter a password to encrypt your token: ")
    encrypted_token = encrypt_token(token, password)
    set_env_variable_permanently(env_var_name, encrypted_token)
    os.environ[env_var_name] = encrypted_token
    logging.info(f"Encrypted GitHub token stored in environment variable {env_var_name}.")

    return token
