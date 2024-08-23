import requests
import os
import logging

def slugify(title):
    return title.lower().replace(' ', '-').replace('.', '').replace(',', '')

def get_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit(0)

def file_exists_on_github(filepath, owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        logging.error(f"Failed to check if file exists: {response.json()}")
        return False
