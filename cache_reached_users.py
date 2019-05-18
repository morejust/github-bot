import os
import random

from githubbot import GithubBot

with GithubBot(
    username=os.environ.get('GITHUB_USERNAME'),
    password=os.environ.get('GITHUB_TOKEN')
) as gh:
    gh.update_reached_users()