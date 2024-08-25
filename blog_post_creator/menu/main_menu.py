from blog_post_creator.infrastructure.config_manager import ConfigManager
from blog_post_creator.infrastructure.input_handler import InputHandler
from blog_post_creator.services.token_service import TokenService
from blog_post_creator.domain.post_manager import PostManager
from blog_post_creator.utils.error_handler import handle_error
from blog_post_creator.menu.configuration_menu import configuration_menu

def main_menu(config_manager: ConfigManager, input_handler: InputHandler, token_service: TokenService, post_manager: PostManager):
    """Main menu for the application."""
    while True:
        print("\nPlease choose an option:")
        print("1. Create a blog post")
        print("2. Reset GitHub token")
        print("3. Reset password for GitHub token decryption")
        print("4. Configure Settings")
        print("5. Exit")
        
        choice = input_handler.get_input("Enter your choice (1-5): ")

        if choice == "1":
            try:
                post_manager.create_post()
            except Exception as e:
                handle_error(e)
        elif choice == "2":
            try:
                token_service.encrypt_and_store_token()
            except Exception as e:
                handle_error(e)
        elif choice == "3":
            try:
                token_service.reset_password()
            except Exception as e:
                handle_error(e)
        elif choice == "4":
            configuration_menu(config_manager, input_handler)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
