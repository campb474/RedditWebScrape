import requests
from dotenv import load_dotenv
import os

class redditScrape:

    # Initializes environemnt variables and reddit api connection
    def __init__(self):
        # Getting secure information form environment file
        load_dotenv()
        self.PASSWORD = os.environ.get("password")
        self.USERNAME = os.environ.get("username")
        self.CLIENT_ID = os.environ.get("CLIENT_ID")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")

        # Getting authorization token
        auth = requests.auth.HTTPBasicAuth(self.CLIENT_ID, self.SECRET_KEY)
        data = {
            'grant_type': 'password',
            'username': self.USERNAME,
            'password': self.PASSWORD,
        }
        self.headers = {'User-Agent': 'MyBot/0.0.1'}
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.headers)
        self.TOKEN = res.json()['access_token']
        self.headers['authorization'] = f'bearer {self.TOKEN}'

        # Initializing pandas dataframe for recording posts
        self.posts = {}

        # Accessing Reddit API
        # <Response [403]> -> indicates error
        # <Response [200]> -> indicates that everything is fine
        print(requests.get("https://oauth.reddit.com/api/v1/me", headers=self.headers))
        return


    # Parameters
    #   1. sub (str) -> subreddit to find popular posts on
    def getPopular(self, sub: str) -> any:
        res = requests.get('https://oauth.reddit.com/r/' + sub + '/hot', headers=self.headers)
        self.posts[sub] = {}
        print(res.json())
        for post in res.json()['data']['children']:
            self.posts[sub][post['data']['subreddit']] = {
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score']
            }

        print(self.posts)
        return

def main():
    reddit = redditScrape()
    reddit.getPopular('boysvsgirlsmemes')


main()
