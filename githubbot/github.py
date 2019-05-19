import os
import time
import random
import requests
from tqdm import tqdm

GITHUB_API_URL = 'https://api.github.com'

class Github:
    def __init__(self, username: str, password: str) -> None:
        if username is None or password is None:
            raise RuntimeError("Provide valid credentials.")

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.username = username

    def _handle_http_errors(self, response: requests.Response) -> None:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise RuntimeError(
                f"HTTP Error! Status code: {response.status_code}", response.status_code
            ) from http_error
                
    def _get_followers_or_following(self, username: str, followers_or_following: str):
        if followers_or_following not in ["followers", "following"]:
            raise RuntimeError(
                f"Param can be only 'followers' or 'following' (not {followers_or_following})"
            )
            
        api_route = 'user' if username == self.username else f'users/{username}'
        current_url = f'{GITHUB_API_URL}/{api_route}/{followers_or_following}?page=1'

        result = set()
        while True:
            current_response = self.session.get(current_url, timeout=5)
            self._handle_http_errors(current_response)

            result |= set([follower["login"] for follower in current_response.json()])

            try:
                current_url = current_response.links["next"]["url"]
            except KeyError:
                break
                
        return result
        
    def get_followers(self, username: str):
        return self._get_followers_or_following(username, followers_or_following="followers")
    
    def get_following(self, username: str):
        return self._get_followers_or_following(username, followers_or_following="following")
        
    def follow(self, username: str):
        response = self.session.put(
            f"{GITHUB_API_URL}/user/following/{username}", timeout=5
        )
        self._handle_http_errors(response)
        return response
    
    def unfollow(self, username: str):
        response = self.session.delete(
            f"{GITHUB_API_URL}/user/following/{username}", timeout=5
        )
        self._handle_http_errors(response)
        return response

    def __del__(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()