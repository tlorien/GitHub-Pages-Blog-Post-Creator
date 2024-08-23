import logging
from datetime import datetime
from blog_post_creator.config import handle_encrypted_token, load_config
from blog_post_creator.utils import slugify, get_input, file_exists_on_github
from blog_post_creator.github_client import push_to_github

config = load_config("config/config.ini")

# Constants
REPO_OWNER = config["github"]["repo_owner"]
REPO_NAME = config["github"]["repo_name"]
BRANCH = config["github"]["branch"]
POSTS_DIR = config["post"]["posts_dir"]

# Template
TEMPLATE = """---
layout: post
title: "{title}"
date: {date}
author: {author}
categories: {categories}
tags: {tags}
excerpt: "{excerpt}"
---
# {title}

{content}
"""

def create_post():
    title = get_input("Enter the post title: ")
    author = get_input("Enter the author's name: ")
    categories = get_input("Enter the categories (comma-separated): ")
    tags = get_input("Enter the tags (comma-separated): ")
    excerpt = get_input("Enter a short excerpt: ")
    content = get_input("Enter the main content: ")

    today = datetime.now().strftime('%Y-%m-%d')
    post_number = 1
    github_token = None

    while True:
        filename = f"{today}-{post_number}.md"
        filepath = f"{POSTS_DIR}/{filename}".replace("\\", "/")

        if github_token is None:
            github_token = handle_encrypted_token('BLOG_POST_CREATOR_GITHUB_TOKEN')
            logging.debug(f"Using decrypted GitHub token: {github_token}")
       
        logging.info(f"Checking if file exists: {filepath} in repository {REPO_OWNER}/{REPO_NAME}")

        if not file_exists_on_github(filepath, REPO_OWNER, REPO_NAME, github_token):
            break
        post_number += 1

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_content = TEMPLATE.format(
        title=title,
        date=date,
        author=author,
        categories=categories,
        tags=tags,
        excerpt=excerpt,
        content=content
    )

    while not push_to_github(filepath, post_content, github_token, REPO_OWNER, REPO_NAME, BRANCH):
        logging.error("Failed to create post due to an invalid token.")
        github_token = handle_encrypted_token('BLOG_POST_CREATOR_GITHUB_TOKEN', invalid_token=True)
        logging.debug(f"Retrying with new decrypted token: {github_token}")

        post_number = 1
        while True:
            filename = f"{today}-{post_number}.md"
            filepath = f"{POSTS_DIR}/{filename}".replace("\\", "/")

            if not file_exists_on_github(filepath, REPO_OWNER, REPO_NAME, github_token):
                break
            post_number += 1

    logging.info(f"Post successfully created and pushed to GitHub: {filepath}")
    print(f"Post '{filename}' was successfully created and pushed to GitHub.")