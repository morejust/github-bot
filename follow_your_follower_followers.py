import os
import random

from githubbot import GithubBot

with GithubBot(
    username=os.environ.get('GITHUB_USERNAME'),
    password=os.environ.get('GITHUB_TOKEN')
) as gh:
    # gh.update_reached_users()
    my_followers = gh.api.get_followers(gh.username)
    username = random.sample(my_followers, 1)[0]

    print("Going to follow %s's followers:" % username)
    gh.follow_user_followers(username)