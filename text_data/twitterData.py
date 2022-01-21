import tweepy
import pandas as pd
import re

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
# Store the tweets in a variable and get the full text
all_tweets = [tweet.full_text for tweet in tweets]
# Create a dataframe to store the tweets with a column called 'Tweets'
df = pd.DataFrame(all_tweets, columns=["Tweets"])
print(df)
# Show the first 5 rows
df.head(5)

# Create a function to clean the tweets
def cleanTweet(tweet):
    temp = re.sub("@[A-Za-z0-9_]+", "", tweet)
    temp = re.sub("#[A-Za-z0-9_]+", "", temp)
    # temp = re.sub("#bitcoin", "bitcoin", temp)  # Remove the '#' from bitcoin
    # temp = re.sub("#Bitcoin", "Bitcoin", temp)  # Remove the '#' from Bitcoin
    # temp = re.sub("#[A-Za-z0-9]+", "", temp)  # Remove any strings with a '#'
    temp = re.sub("\\n", " ", temp)  # Remove the '\n'
    temp = re.sub(r"https\S+", "", temp)  # Remove any hyperlinks
    temp = re.sub(r"http\S+", "", temp)
    temp = re.sub(r"www.\S+", "", temp)
    return temp


# Clean the tweets
df["Cleaned_Tweets"] = df["Tweets"].apply(cleanTweet)
# Show the dataset
print(df.head())
