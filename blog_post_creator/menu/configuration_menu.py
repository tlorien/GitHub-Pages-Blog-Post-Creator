from blog_post_creator.infrastructure.config_manager import ConfigManager
from blog_post_creator.infrastructure.input_handler import InputHandler
from blog_post_creator.utils.error_handler import handle_error
from blog_post_creator.blog_post_creator.utils.errors import ConfigError

def configuration_menu(config_manager: ConfigManager, input_handler: InputHandler):
    """Interactive menu to configure settings."""
    while True:
        print("\nConfiguration Settings:")
        print("1. Set GitHub Repository Owner")
        print("2. Set GitHub Repository Name")
        print("3. Set Default Branch")
        print("4. Set Default Post Directory")
        print("5. Back to Main Menu")

        choice = input_handler.get_input("Enter your choice (1-5): ")

        try:
            if choice == "1":
                new_owner = input_handler.get_input("Enter new GitHub Repository Owner: ")
                config_manager.update_config('github', 'repo_owner', new_owner)
            elif choice == "2":
                new_repo = input_handler.get_input("Enter new GitHub Repository Name: ")
                config_manager.update_config('github', 'repo_name', new_repo)
            elif choice == "3":
                new_branch = input_handler.get_input("Enter new Default Branch: ")
                config_manager.update_config('github', 'branch', new_branch)
            elif choice == "4":
                new_post_dir = input_handler.get_input("Enter new Default Post Directory: ")
                config_manager.update_config('content', 'default_post_directory', new_post_dir)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ConfigError as e:
            handle_error(e)
            print(f"Failed to update configuration: {e}")

