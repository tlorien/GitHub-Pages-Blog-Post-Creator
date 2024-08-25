import configparser
import os
import logging
from blog_post_creator.blog_post_creator.utils.errors import ConfigError
from blog_post_creator.utils.error_handler import handle_error
from blog_post_creator.infrastructure.input_handler import InputHandler

class ConfigManager:
    def __init__(self, config_file='config/config.ini', input_handler=None):
        self.config_file = config_file
        self.input_handler = input_handler or InputHandler()
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from the config file and validate necessary values."""
        config = configparser.ConfigParser()

        if not os.path.exists(self.config_file):
            logging.warning(f"Configuration file {self.config_file} not found. Creating a new one with default values.")
            self.create_default_config()

        try:
            config.read(self.config_file)
            self.validate_and_prompt_config(config)
        except Exception as e:
            handle_error(e)
            raise ConfigError(f"Failed to load configuration: {e}")

        return config

    def validate_and_prompt_config(self, config):
        """Validate that the necessary configuration values are present and prompt the user to enter any missing values."""
        required_sections = ['github']
        required_keys = {
            'github': ['repo_owner', 'repo_name', 'branch']
        }

        for section in required_sections:
            if section not in config:
                logging.warning(f"Missing required section: [{section}] in configuration. Adding section.")
                config.add_section(section)

            for key in required_keys[section]:
                if key not in config[section] or not config[section][key]:
                    logging.warning(f"Missing required key: '{key}' in section [{section}] of configuration.")
                    value = self.input_handler.get_input(f"Please enter a value for '{key}' in section [{section}]: ")
                    config[section][key] = value

        self.save_config(config)

    def update_config(self, section, key, value):
        """Update a specific configuration value and save the configuration file."""
        try:
            if section not in self.config:
                self.config.add_section(section)
            self.config[section][key] = value
            self.save_config(self.config)
            logging.info(f"Configuration updated: [{section}] {key} = {value}")
        except Exception as e:
            handle_error(e)
            raise ConfigError(f"Failed to update configuration: {e}")

    def save_config(self, config):
        """Save the current configuration to the config file."""
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
        logging.info(f"Configuration updated and saved to {self.config_file}.")

    def create_default_config(self):
        """Create a default configuration file with placeholder values."""
        config = configparser.ConfigParser()

        config['github'] = {
            'repo_owner': '',
            'repo_name': '',
            'branch': ''
        }

        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
        logging.info(f"Default configuration created at {self.config_file}.")

    def get(self):
        """Return the loaded configuration."""
        return self.config
