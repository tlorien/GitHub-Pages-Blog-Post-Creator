# GitHub Pages Blogger

The **GitHub Pages Blogger** is a simple Python program designed to automate the creation and uploading of blog posts to a GitHub Pages repository. It utilizes GitHub tokens securely by storing them as encrypted environment variables, which are decrypted by a password that is not stored on your machine.

This script is intended to be utilized with Jekyll [(click here to learn how to create your own GitHub Page)](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll).

## Features

- **Create New Blog Posts**: Input blog details such as title, author, categories, tags, and content directly from the command line. Posts are saved to the '_posts' folder at the root of the repository, as per Jekyll's expected conventions.
- **Secure Token Management**: Encrypts and stores GitHub tokens securely as environment variables.
- **Automatic File Name Incrementing**: Automatically checks for existing blog files on GitHub and increments the file name to avoid overwriting.
- **Token and Password Management**: Allows resetting of GitHub tokens and passwords when necessary.
- **GitHub Integration**: Directly uploads the blog post to a configured GitHub repository branch.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/tlorien/GitHub-Pages-Blogger.git
cd GitHub-Pages-Blogger
```

2. **Install the required Python packages:** Ensure you have Python 3.x installed and run:

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Script:**

Click main.py, or type in the console:

```bash
python main.py
```

2. Choose an Option:

- 1: Create a new blog post
- 2: Reset GitHub token
- 3: Reset password
- 4: Exit

Follow Prompts: Depending on your choice: create a blog post, reset your GitHub token, or change your password.

## Configuration


**config/config.ini:** Configuration file to set repository details such as repo_owner, repo_name, branch, and posts_dir. This file is automatically created if it does not exist, and users will be prompted to fill in missing values.

## Environment Variables

**BLOG_POST_CREATOR_GITHUB_TOKEN:** The GitHub token encrypted and stored as a user environment variable. It is used to authenticate API requests to GitHub to both make push requests and check for existing file names to prevent overwrites.

## Requirements

- Python 3.x
- The required Python packages are listed in **requirements.txt**.

## Contributing

Feel free to fork this repository and submit pull requests. Thanks for reading, happy blogging!

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
