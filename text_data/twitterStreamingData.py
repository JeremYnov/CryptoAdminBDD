import tweepy
import pandas as pd 

# Store the data
log = pd.read_csv("./Login.csv")
# Get the twitter API credentials
consumerKey = log["key"][0]
consumerSecret = log["key"][1]
accessToken = log["key"][2]
accessTokenSecret = log["key"][3]

# Create the authentication object
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
# Set the access token and the access token secret
auth.set_access_token(accessToken, accessTokenSecret)
# Create the API object
api = tweepy.API(auth, wait_on_rate_limit=True)
# Gather 2000 tweets about Bitcoin  and filter out any retweets 'RT'
search_term = "#bitcoin -filter:retweets"
# Create a cursor object
tweets = tweepy.Cursor(
    api.search_tweets,
    q=search_term,
    lang="en",
    tweet_mode="extended",
    result_type="recent",
).items(100)