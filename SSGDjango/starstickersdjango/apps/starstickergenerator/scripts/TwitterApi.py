# Tweetpy
import tweepy

# Settings
from django.conf import settings

# Credentials
from ..credentials import TWITTER_CREDENTIALS


class TwitterAPI():

    # Consumer keys and access tokens, used for OAuth
    consumer_key = TWITTER_CREDENTIALS['consumer_key']
    consumer_secret = TWITTER_CREDENTIALS['consumer_secret']
    access_token = TWITTER_CREDENTIALS['access_token']
    access_token_secret = TWITTER_CREDENTIALS['access_token_secret']

    def GetGraphInstance(self):
        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        # Creation of the actual interface, using authentication
        api = tweepy.API(auth)
        return api

    def PostImage(self, img_path=settings.STATIC_IMAGE_FOLDER + "/image_generated.png",
                  status_text="#starstickersforeverything"):
        api = self.GetGraphInstance()
        user = api.me()
        # load image
        imagePath = img_path
        status = status_text
        # Send the tweet.
        # api.update_status(status="[this tweet is a test]")
        api.update_with_media(imagePath, status)
        data = {
            'user': user.name,
            'posted': True
        }
        return data

# EXAMPLE:
# a = TwitterAPI()
# a.PostImage()
