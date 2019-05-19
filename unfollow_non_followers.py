import os

from githubbot import GithubBot

with GithubBot(
    username=os.environ.get('GITHUB_USERNAME'),
    password=os.environ.get('GITHUB_TOKEN')
) as gh:
    gh.unfollow_non_followers()