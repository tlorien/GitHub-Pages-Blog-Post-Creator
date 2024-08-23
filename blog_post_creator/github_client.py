import base64
import requests
import logging

def push_to_github(filepath, content, token, owner, repo, branch):
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    logging.info(f"Attempting to push to URL: {url}")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    logging.info(f"Using token: {token}")
    get_response = requests.get(url, headers=headers)
    logging.info(f"GitHub GET response status: {get_response.status_code}")

    if get_response.status_code == 200:
        sha = get_response.json()['sha']
        data = {
            "message": f"Update post: {filepath}",
            "content": encoded_content,
            "branch": branch,
            "sha": sha
        }
    elif get_response.status_code == 404:
        data = {
            "message": f"Add new post: {filepath}",
            "content": encoded_content,
            "branch": branch
        }
    else:
        logging.error(f"Failed to check if file exists: {get_response.json()}")
        return False

    response = requests.put(url, json=data, headers=headers)
    logging.info(f"GitHub PUT response status: {response.status_code}")

    if response.status_code in [200, 201]:
        return True
    else:
        logging.error(f"Failed to create post: {response.json()}")
        return False
