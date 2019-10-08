import os
import random
import datetime

from githubbot import GithubBot

weekno = datetime.datetime.today().weekday()

FOLLOWERS_TO_FOLLOW_THEIR_FOLLOWERS = 2

with GithubBot(
    username=os.environ.get('GITHUB_USERNAME'),
    password=os.environ.get('GITHUB_TOKEN')
) as gh:
    if weekno < 5:
        my_followers = gh.api.get_followers(gh.username)
        users = random.sample(
            my_followers, FOLLOWERS_TO_FOLLOW_THEIR_FOLLOWERS
        )

        for username in users:
            print("Going to follow %s's followers:" % username)
            gh.follow_user_followers(username)

    else:
        gh.unfollow_everyone()