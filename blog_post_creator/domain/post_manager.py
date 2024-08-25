from datetime import datetime 
from blog_post_creator.services.github_service import GitHubService
from blog_post_creator.infrastructure.input_handler import InputHandler

class PostManager:
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

    def __init__(self, config, github_service: GitHubService, input_handler: InputHandler):
        self.config = config
        self.github_service = github_service
        self.input_handler = input_handler

    def create_post(self):
        title = self.input_handler.get_input("Enter the post title: ")
        author = self.input_handler.get_input("Enter the author's name: ")
        categories = self.input_handler.get_input("Enter the categories (comma-separated): ")
        tags = self.input_handler.get_input("Enter the tags (comma-separated): ")
        excerpt = self.input_handler.get_input("Enter a short excerpt: ")
        content = self.input_handler.get_input("Enter the main content: ")

        today = datetime.now().strftime('%Y-%m-%d')
        post_number = 1

        while True:
            filename = f"{today}-{post_number}.md"
            filepath = f"{self.config['post']['posts_dir']}/{filename}".replace("\\", "/")

            if not self.github_service.file_exists_on_github(filepath):
                break
            post_number += 1

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post_content = self.TEMPLATE.format(
            title=title,
            date=date,
            author=author,
            categories=categories,
            tags=tags,
            excerpt=excerpt,
            content=content
        )

        self.github_service.push_post_to_github(filepath, post_content)
        print(f"Post '{filename}' was successfully created and pushed to GitHub.")
