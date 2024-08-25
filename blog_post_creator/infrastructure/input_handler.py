import getpass

class InputHandler:
    @staticmethod
    def get_input(prompt: str) -> str:
        """Get general input from the user."""
        try:
            return input(prompt)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit(0)

    @staticmethod
    def get_secure_input(prompt: str) -> str:
        """Get secure input (e.g., tokens or passwords) from the user without echoing to the console."""
        try:
            return getpass.getpass(prompt)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit(0)
