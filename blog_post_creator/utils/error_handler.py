import logging

def handle_error(error):
    """Centralized error handling function."""
    logging.error(f"Error: {str(error)}")
    print(f"An error occurred: {str(error)}. Please check the logs for more details.")
