import tweepy
from textblob import TextBlob
import pandas as pd

# import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")
# Store the data
log = pd.read_csv("Login.csv")
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
    tweet = re.sub("#bitcoin", "bitcoin", tweet)  # Remove the '#' from bitcoin
    tweet = re.sub("#Bitcoin", "Bitcoin", tweet)  # Remove the '#' from Bitcoin
    tweet = re.sub("#[A-Za-z0-9]+", "", tweet)  # Remove any strings with a '#'
    tweet = re.sub("\\n", " ", tweet)  # Remove the '\n'
    tweet = re.sub(r"https?:\/\/S+", "", tweet)  # Remove any hyperlinks
    return tweet


# Clean the tweets
df["Cleaned_Tweets"] = df["Tweets"].apply(cleanTweet)
# Show the dataset
df.head()


# Create a function to get the subjectivity
def getSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity


# Create two new columns
df["Subjectivity"] = df["Cleaned_Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Cleaned_Tweets"].apply(getPolarity)
df.head()


# Create a function to get the sentiment text
def getSentiment(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


df["Sentiment"] = df["Polarity"].apply(getSentiment)
df.head()
# Create a scatter plot to show the subjectivity and the polarity
plt.figure(figsize=(8, 6))
for i in range(0, df.shape[0]):
    plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color="Purple")
plt.title("Sentiment Analysis Scatter Plot")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity (Objective => Subjective")
plt.show()

# Create a bar chart to show the count of Positive, Neutral and Negative sentiments
df["Sentiment"].value_counts().plot(kind="bar")
plt.title("Sentiment Analysis Bar Plot")
plt.xlabel("Sentiment")
plt.ylabel("Number of tweets")
plt.show()