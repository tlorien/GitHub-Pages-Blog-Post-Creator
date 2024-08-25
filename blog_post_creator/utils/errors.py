class BlogPostCreatorError(Exception):
    """Base class for all exceptions raised by the blog post creator application."""
    pass

class ConfigError(BlogPostCreatorError):
    """Exception raised for errors related to configuration management."""
    def __init__(self, message="Configuration error occurred"):
        self.message = message
        super().__init__(self.message)

class GitHubServiceError(BlogPostCreatorError):
    """Exception raised for errors related to GitHub service operations."""
    def __init__(self, message="GitHub service error occurred"):
        self.message = message
        super().__init__(self.message)

class EncryptionError(BlogPostCreatorError):
    """Exception raised for errors related to encryption and decryption operations."""
    def __init__(self, message="Encryption error occurred"):
        self.message = message
        super().__init__(self.message)

class InputError(BlogPostCreatorError):
    """Exception raised for errors related to user input operations."""
    def __init__(self, message="Input error occurred"):
        self.message = message
        super().__init__(self.message)

class MissingConfigValueError(ConfigError):
    """Exception raised for missing configuration values."""
    def __init__(self, message="Configuration value is missing"):
        self.message = message
        super().__init__(self.message)