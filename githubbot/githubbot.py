import os
import time
import random
from tqdm import tqdm

from .github import Github

class GithubBot:
    def __init__(self, username, password):
        self.api = Github(username, password)

        self.username = username
        self.reached_users = self._read_reached_users()

    def _read_reached_users(self):
        filename ="%s.txt" % self.username

        if not os.path.isfile(filename):
            return set()

        with open(filename, 'r') as fhandle:  
            return set([line.rstrip() for line in fhandle.readlines()])

    def _dump_reached_users(self):
        filename = "%s.txt" % self.username

        with open(filename, 'w') as fhandle:
            fhandle.writelines("%s\n" % user for user in self.reached_users)  
        
    def follow(self, username):
        self.api.follow(username)
        self.reached_users.add(username)
        self.sleep()
        
    def unfollow(self, username):
        self.api.unfollow(username)
        self.reached_users.add(username)
        self.sleep()
        
    def sleep(self, max_val=30, min_val=3):
        time.sleep(min_val + max_val * random.random())
        
    def update_reached_users(self):
        self.reached_users |= self.api.get_followers(self.api.username) | self.api.get_following(self.api.username)
        print("Users reached: %d" % len(self.reached_users))
        self._dump_reached_users()
        
    def follow_user_followers(self, username):
        followers = self.api.get_followers(username)
        for user_to_follow in tqdm(
            followers, 
            total=len(followers),
            desc="%s's followers" % username
        ):
            self.follow(user_to_follow)
            
    def unfollow_everyone(self):
        my_followings = self.api.get_following(self.api.username)
        for user_to_unfollow in tqdm(my_followings):
            self.unfollow(user_to_unfollow)

    def unfollow_non_followers(self):
        my_followings = self.api.get_following(self.api.username)
        my_followers = self.api.get_followers(self.api.username)
        for user_to_unfollow in tqdm(my_followings):
            if user_to_unfollow in my_followers:
                continue
            self.unfollow(user_to_unfollow)

    def unfollow_followers(self):
        my_followings = self.api.get_following(self.api.username)
        my_followers = self.api.get_followers(self.api.username)
        for user_to_unfollow in tqdm(my_followings):
            if user_to_unfollow not in my_followers:
                continue
            self.unfollow(user_to_unfollow)

    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self._dump_reached_users()
