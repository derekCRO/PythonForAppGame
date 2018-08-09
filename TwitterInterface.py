from twitter import *

"""
consumer_key = 	"iNz44Fzfd0qlUoac4tTNJUSSz"
consumer_secret = "hZ5EvltaPoumKmz3E6yqLwU5054xc80FDZ8EMMH6PaAGgB79gw"
token = "962017577114394624-j2tLDh7yqiq9RSW2OV14zfMmukMhwW1"
token_secret = "8hVhTOi7eTLdjBHiTIRelM1WPMP3hXHHu37w84yxqM3lV"

twitterFeed = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
"""

class TwitterInterface():
    def __init__(self):
        self.consumer_key = ""
        self.consumer_secret = ""
        self.token = ""
        self.token_secret = ""
        self.twitterFeed = None

    def connectToTwitter(self, _consumer_key, _consumer_secret, _token, _token_secret):
        self.consumer_key = _consumer_key
        self.consumer_secret = _consumer_secret
        self.token = _token
        self.token_secret = _token_secret
        self.twitterFeed = Twitter(auth=OAuth(self.token, self.token_secret, self.consumer_key, self.consumer_secret))

    def postToTwitter(self, stringToPost):

        if(self.twitterFeed != None):
            self.twitterFeed.statuses.update(status=stringToPost)