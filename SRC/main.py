import requests
from dotenv import load_dotenv
import os

# Getting secure information form environment file
load_dotenv()
PASSWORD = os.environ.get("password")
USERNAME = os.environ.get("username")
CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Getting authorization token
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD,
}
headers = {'User-Agent': 'MyBot/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['authorization'] = f'bearer {TOKEN}'

# Accessing Reddit API
# <Response [403]> -> indicates error
# <Response [200]> -> indicates that everything is fine
print(requests.get("https://oauth.reddit.com/api/v1/me", headers=headers))