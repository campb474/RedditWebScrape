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

        # Accessing Reddit API
        # <Response [403]> -> indicates error
        # <Response [200]> -> indicates that everything is fine
        print(requests.get("https://oauth.reddit.com/api/v1/me", headers=self.headers))

def main():
    reddit = redditScrape()

main()
