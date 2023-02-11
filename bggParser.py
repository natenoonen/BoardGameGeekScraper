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

    all_games = {}
    parser = MyHTMLParser()
    backoff = 1
    for i in range(1, 10):
        user_agent = random.choice(user_agent_list)
        page_uri = "https://boardgamegeek.com/browse/boardgame/page/{0}".format(i)
        headers = {
            'User-Agent': user_agent}
        r = requests.Session()
        response = r.get(page_uri, headers=headers)
        body = response.content.decode()
        parser.feed(body)
        # print(parser.games)
        for gameId in parser.games:
            r2 = requests.Session()
            page_uri2 = "https://boardgamegeek.com/xmlapi2/thing?id={0}&stats=1".format(gameId)
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
                ranks = doc.findall('./item/statistics/ratings/ranks/rank')
                for rank in ranks:
                    if rank.get('friendlyname') == 'Board Game Rank':
                        bgg_rank = rank.get('value')
                        # print(bgg_rank)
                names = doc.findall('./item/name')
                for name in names:
                    if name.get('type') == 'primary':
                        bgg_name = name.get('value')
                all_games[gameId] = BoardGame(gameId, bgg_name, bgg_rank)
            else:
                if backoff == 10:
                    print('F You BGG RATE LIMIT')
                    backoff = 30
                else:
                    print('Oh Noes')
                    backoff = 10
                time.sleep(backoff)
    for game in all_games:
        local_g = all_games[game]
        print("{0},{1},{2}".format(local_g.Id, local_g.Name, local_g.Rank))
if __name__ == "__main__":
    main(sys.argv[1:])
