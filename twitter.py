"""
Task 1: Twitter Wars!
=====================

Get twitts
----------
I've use the twitter API and in particular the ``geocode`` argument in order
to get twitts from a specific region. London and Exeter are defined as a
point and an approximate radious.

Clean twitts
------------
To clean the twitts text I've use a couple of regexp to remove mentions, urls,
hashtags and phone numbers.

Analize twitts
--------------
Calling an external API to determine if a word is correct or not could be
really expensive, so I've use the internal dictionary all unix distributions
use to do spellcheking. This ara huge files containing common English words
and names. I'm using Mac and these files are located in ``/usr/share/dict/``,
if you are using any other linux distribution you should specify where these
files are.

For every of these files I create a ``Dictionary`` object I'll use later to
check if every word inside the tweet is "valid" or not.

For every word in the text I call `Dictionary.score`` to check if it's valid
or not using `0` as not found score. As soon as a dictionary scores a word I
don't score it again.

Every Dictionary has different multipliers so, ``connectives`` only score ``0.5``
and more complex words (like the ones inside ``web2``) score ``2``.

The score is based on the multiplication of the len of the word and the
dictionary multiplier.

The city that gets a higher score, Wins!

Usage
-----

$python twitter.py [--count NUMBER]

You can use ``--count`` to choose how many twitts you want to process.

Requirements
-------------

You should have ``requests`` installed.

"""

import os
import re
import requests
import argparse

LONDON = '51.507222,-0.1275,14mi'
EXETER = '50.716667,-3.533333,5mi'


class Dictionary(object):
    """"""
    def __init__(self, path, multiplier=1):
        self.path = path
        self.multiplier = multiplier

        with open(self.path, 'r') as f:
            self.words = f.read().split('\n')

    def score(self, word):
        if word in self.words:
            return len(word) * self.multiplier
        return 0


class Analizer(object):

    twitter_endpoint = 'http://search.twitter.com/search.json?geocode={0}&lang=en&page={1}'
    dicts_path = '/usr/share/dict/'
    dicts = {'connectives': 0.5,
             'propernames': 1,
             'web2': 2,
             'web2a': 2}

    clean_rules = [r'^RT\s',   # Old style retweet messages
                   r'\/via',   # /via ...
                   r'\@\w+',   # @username
                   r'\#\w+',   # #hashtag
                   r'\d+',     # phone numbers
                   r'\&\w+;',  # Ignore scaped text
                   r'https?\:\/\/[^\s]+']  # URL's

    def __init__(self):
        self.dictionaries = []
        for dictionary, score in self.dicts.iteritems():
            path = os.path.join(self.dicts_path, dictionary)
            self.dictionaries.append(Dictionary(path, score))

    def extract_words(self, text):
        """Clean a text using clean_rules in order
           to only analize proper words"""

        for rule in self.clean_rules:
            text = re.sub(rule, '', text)
        text = re.sub(r'[^\w\' ]', ' ', text)
        words = text.split(' ')
        return filter(lambda w: w, words)

    def score(self, words):
        total = 0
        for word in words:
            for dictionary in self.dictionaries:
                points = dictionary.score(word)
                if points:
                    total += points
                else:
                    break
        return total / len(words)

    def analize_city(self, name, city, count=10):
        print name
        print "#" * 50

        city_score = 0
        for message, words in self.get_twitter_messages(city, count):
            message_score = self.score(words)
            city_score += message_score
            print "(%.2f) %s" % (message_score, message)

        return city_score

    def get_twitter_messages(self, city, count=10):
        total = 0
        page = 1

        while total < count:
            tweets = requests.get(self.twitter_endpoint.format(city, page))
            for message in tweets.json()['results']:
                words = self.extract_words(message['text'])
                # Check if the tweet was not full of crap
                if words:
                    if total == count:
                        break
                    total += 1

                    yield message['text'].replace('\n', ''), words

            page += 1


def main(count):
    an = Analizer()
    london_score = an.analize_city('London', LONDON, count=count)
    exeter_score = an.analize_city('Exeter', EXETER, count=count)

    print "London score: {0}".format(london_score)
    print "Exeter score: {0}".format(exeter_score)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Twitter Wars!',
                                     description='Process arguments.')
    parser.add_argument('--count', nargs='?', dest='count', type=int,
                        help='Number of twitt to analize', default=10)
    args = parser.parse_args()
    main(args.count)
