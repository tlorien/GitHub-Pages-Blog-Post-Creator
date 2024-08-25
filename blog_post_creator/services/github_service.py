import requests
import base64
import logging
from blog_post_creator.blog_post_creator.utils.errors import GitHubServiceError
from blog_post_creator.utils.error_handler import handle_error
from requests import Session

class GitHubService:
    def __init__(self, token_service, owner, repo, branch, http_client=None):
        self.token_service = token_service
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.http_client = http_client or Session()

    def file_exists_on_github(self, filepath):
        """Check if a file exists on GitHub."""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filepath}"
        headers = {
            "Authorization": f"token {self.token_service.decrypt_token_once()}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            response = self.http_client.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            handle_error(e)
            if e.response.status_code == 404:
                return False
            raise GitHubServiceError(f"Failed to check if file exists due to HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            handle_error(e)
            raise GitHubServiceError("Request failed while checking if file exists on GitHub.")

        logging.debug(f"GitHub GET response status: {response.status_code}")

        try:
            response.json()
        except ValueError as e:
            handle_error(e)
            raise GitHubServiceError(f"Failed to parse JSON response while checking file existence: {e}")

        return response.status_code == 200

    def push_post_to_github(self, filepath, content):
        """Push a new post to GitHub."""
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filepath}"
        headers = {
            "Authorization": f"token {self.token_service.decrypt_token_once()}",
            "Accept": "application/vnd.github.v3+json"
        }

        data = {
            "message": f"Add new post: {filepath}",
            "content": encoded_content,
            "branch": self.branch
        }

        try:
            response = self.http_client.put(url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            handle_error(e)
            raise GitHubServiceError(f"Failed to push post to GitHub due to HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            handle_error(e)
            raise GitHubServiceError("Request failed while pushing post to GitHub.")
        finally:
            self.token_service.clear_decrypted_token()

        logging.debug(f"GitHub PUT response status: {response.status_code}")

        try:
            response.json()
        except ValueError as e:
            handle_error(e)
            raise GitHubServiceError(f"Failed to parse JSON response after pushing to GitHub: {e}")

        return True
