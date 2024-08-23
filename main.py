import logging
from blog_post_creator.config import load_config, handle_encrypted_token, set_env_variable_permanently
from blog_post_creator.utils import get_input
from blog_post_creator.post_manager import create_post
from blog_post_creator.reset_utils import reset_github_token, reset_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
config = load_config("config/config.ini")

def main_menu():
    """
    Display the main menu and handle user input.
    """
    while True:
        print("\nPlease choose an option:")
        print("1. Create a blog post")
        print("2. Reset GitHub token")
        print("3. Reset password")
        print("4. Exit")

        choice = get_input("Enter your choice (1-4): ")

        if choice == "1":
            create_post()
        elif choice == "2":
            reset_github_token()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()
