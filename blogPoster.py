from blog_post_creator.infrastructure.config_manager import ConfigManager
from blog_post_creator.infrastructure.input_handler import InputHandler
from blog_post_creator.infrastructure.logger import Logger
from blog_post_creator.services.github_service import GitHubService
from blog_post_creator.services.encryption_service import EncryptionService
from blog_post_creator.services.token_service import TokenService
from blog_post_creator.domain.post_manager import PostManager
from blog_post_creator.utils.error_handler import handle_error
from blog_post_creator.menu.main_menu import main_menu 
from blog_post_creator.blog_post_creator.utils.errors import ConfigError

def main():
    Logger.setup_logging()

    input_handler = InputHandler()
    
    try:
        config_manager = ConfigManager(input_handler=input_handler)
        config = config_manager.get()
    except ConfigError as e:
        handle_error(e)
        print("Configuration error: Please check your config file and ensure all necessary values are set.")
        return

    encryption_service = EncryptionService()
    token_service = TokenService(encryption_service, input_handler)

    try:
        github_service = GitHubService(
            token_service=token_service,
            owner=config["github"]["repo_owner"],
            repo=config["github"]["repo_name"],
            branch=config["github"]["branch"]
        )
    except Exception as e:
        handle_error(e)
        return

    post_manager = PostManager(config=config, github_service=github_service, input_handler=input_handler)

    main_menu(config_manager, input_handler, token_service, post_manager)

if __name__ == "__main__":
    main()
