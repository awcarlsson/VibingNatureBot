import tweepy
import random

#CONSUMER_KEY = ''
#CONSUMER_SECRET = ''
#ACCESS_KEY = ''
#ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

def main():
    print("Sheesh")
    api.update_status("Testing")
    return 1

main()
