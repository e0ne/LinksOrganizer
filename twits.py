import re

import tweepy

def favorite_twits(page=1):
    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key = ''
    consumer_secret = ''

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located
    # under "Your access token")
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    fav_twits = api.favorites(page=1)
    regexp = r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)'
    twits = []
    for twit in fav_twits:
        if twit.text.find('http') > -1:
            twit.text = re.sub(regexp, update_link_html, twit.text)
            twits.append(twit)
    return twits

def update_link_html(s):
    g = s.group()
    return '<a href="%s" target="_blank">%s</a>' % (g, g)