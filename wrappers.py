import re
import tweepy

import json

class Tweet:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class BaseApiWrapper(object):
    def favorites(self, page=1):
        pass

    def unfavorite(self, id):
            pass


class TwitterApiWrapper(BaseApiWrapper):
    def favorites(self, fav_twits):
        regexp = r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)'
        twits = []
        for t in fav_twits:
            twit = Tweet(**t)
            if twit.text.find('http') > -1:
                twit.text = re.sub(regexp, self.__update_link_html__, twit.text)
                twits.append(twit)
        return twits

    def unfavorite(self, id):
        self.api.destroy_favorite(id)

    def retweet(self, id):
        self.api.retweet(id=id)

    def __update_link_html__(self, s):
        g = s.group()
        return '<a href="%s" target="_blank">%s</a>' % (g, g)


