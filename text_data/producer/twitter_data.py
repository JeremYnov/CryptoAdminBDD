import tweepy
import re

from config_redis import get_value_by_key, var_env

# Create a function to clean the tweets
def cleanTweet(tweet):
    """
    clean text (remove special character)
    args :
        tweet [str] : text
    """
    temp = re.sub("@[A-Za-z0-9_]+", "", tweet)
    temp = re.sub("#[A-Za-z0-9_]+", "", temp)
    # temp = re.sub("#bitcoin", "bitcoin", temp)  # Remove the '#' from bitcoin
    # temp = re.sub("#Bitcoin", "Bitcoin", temp)  # Remove the '#' from Bitcoin
    # temp = re.sub("#[A-Za-z0-9]+", "", temp)  # Remove any strings with a '#'
    temp = re.sub("\\n", " ", temp)  # Remove the '\n'
    temp = re.sub(r"https\S+", "", temp)  # Remove any hyperlinks
    temp = re.sub(r"http\S+", "", temp)
    temp = re.sub(r"www.\S+", "", temp).strip()
    return temp

def get_data_twitter():
    """
    get twitter data
    return [list dict]
    """
    # Get twitter API credentials from redis database
    keys = get_value_by_key(var_env)

    # Get twitter API credentials
    consumerKey = keys["TWITTER_CONSUMER_KEY"]
    consumerSecret = keys["TWITTER_CONSUMER_SECRET"]
    accessToken = keys["TWITTER_ACCESS_TOKEN"]
    accessTokenSecret = keys["TWITTER_ACCESS_TOKEN_SECRET"]

    # Create the authentication object
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and the access token secret
    auth.set_access_token(accessToken, accessTokenSecret)

    # Create the API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Gather 2000 tweets about Bitcoin  and filter out any retweets 'RT'
    # search_terms = ["#bitcoin", "#ethereum", "#solana"]
    search_terms = {
        "BTC": "#bitcoin OR #btc -filter:retweets",
        "ETH": "#ethereum OR #eth  -filter:retweets",
        "SOL": "#solana OR #sol -filter:retweets",
    }

    tweets_by_symbol = []
    for key, value in search_terms.items():
        # Create a cursor object
        tweets = tweepy.Cursor(
            api.search_tweets,
            q=value,
            lang="en",
            tweet_mode="extended",
            result_type="recent",
        ).items(100)
        # clean and add tweets in tweets_by_symbol array in JSON format
        for tweet in tweets:
            tweets_by_symbol.append({"Symbol": key, "Tweet": cleanTweet(tweet.full_text)})

    return tweets_by_symbol

# print(get_data_twitter())
