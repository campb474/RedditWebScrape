import os
import re
import requests
import praw
import configparser
import concurrent.futures
import argparse


class redditImageScraper:
    def __init__(self, sub, limit, order, nsfw=False):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.sub = sub
        self.limit = limit
        self.order = order
        self.nsfw = nsfw
        self.path = f'images/{self.sub}/'
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'],
                                  client_secret=config['REDDIT']['client_secret'],
                                  user_agent='MyBot/0.0.1')

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            go = 0
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None)
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)

            for submission in submissions:
                if not submission.stickied  \
                    and submission.url.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + re.search('(?s:.*)\w/(.*)', submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname})
                        go += 1
                        if go >= self.limit:
                            break
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)


def main():
    parser = argparse.ArgumentParser(description='')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-s', type=str, help="subreddit", required=True)
    required_args.add_argument('-i', type=int, help="number of images", required=True)
    required_args.add_argument('-o', type=str, help="order (new/top/hot)", required=True)
    args = parser.parse_args()
    scraper = redditImageScraper(args.s, args.i, args.o)
    scraper.start()
    print("\nImages added successfully\n")


if __name__ == '__main__':
    main()
