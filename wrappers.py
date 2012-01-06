import re
import tweepy

class BaseApiWrapper(object):
    def favorites(self, page=1):
        pass

    def unfavorite(self, id):
            pass


class TwitterApiWrapper(BaseApiWrapper):
    def __init__(self, ckey, csecret, atoken, asecret):
        # The consumer keys can be found on your application's Details
        # page located at https://dev.twitter.com/apps (under "OAuth settings")
        consumer_key = ckey
        consumer_secret = csecret

        # The access tokens can be found on your applications's Details
        # page located at https://dev.twitter.com/apps (located
        # under "Your access token")
        access_token = atoken
        access_token_secret = asecret

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def favorites(self, page=1):
        fav_twits = self.api.favorites(page=1)
        regexp = r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)'
        twits = []
        for twit in fav_twits:
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


