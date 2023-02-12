#!/usr/bin/python

import requests
import sys
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import time
# import re
import random


class BoardGame:
    def __init__(self, id, name, rank):
        self.Id = id
        self.Rank = rank
        self.Name = name


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.games = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[1] == "primary":
                    split = attrs[0][1].split('/')
                    self.games.append(split[2])


def main(argv):
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    user_name = 'flipflopsnowman'
    if len(argv) > 0:
        user_name = argv[0]
    all_games = {}
    backoff = 1

    r2 = requests.Session()
    page_uri2 = "https://boardgamegeek.com/xmlapi2/collection?username={0}&stats=1".format(user_name)
    user_agent = random.choice(user_agent_list)
    headers2 = {
        'User-Agent': user_agent}
    response2 = r2.get(page_uri2, headers=headers2)
    if response2.ok:
        backoff = 1
        bgg_name = ""
        bgg_rank = 0
        body2 = response2.content.decode()
        doc = ET.fromstring(body2)

        games = doc.findall('./item')
        for game in games:
            if game.get('subtype') == 'boardgame':
                ratings = game.findall('stats/rating')
                for rating in ratings:
                    gameRating = rating.get('value')
                gameId = game.get('objectid')
                print(gameId)
                print(gameRating)
    else:
        if backoff == 10:
            print('F You BGG RATE LIMIT')
            backoff = 30
        else:
            print('Oh Noes')
            backoff = 10
        time.sleep(backoff)
if __name__ == "__main__":
    main(sys.argv[1:])
