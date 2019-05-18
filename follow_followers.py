import os
import sys

from githubbot import GithubBot

if len(sys.argv) != 2:
    print("Usage: %s <GitHub username to follow his/her followers>" % (sys.argv[0]))

username = sys.argv[1]
print("Going to follow %s's followers:" % username)

with GithubBot(
    username=os.environ.get('GITHUB_USERNAME'),
    password=os.environ.get('GITHUB_TOKEN')
) as gh:
    gh.follow_user_followers(username)