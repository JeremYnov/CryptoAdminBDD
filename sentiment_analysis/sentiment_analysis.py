import os
from dotenv import load_dotenv
from pymongo import MongoClient
import time
from textblob import TextBlob
from bson.objectid import ObjectId

load_dotenv()

# # get database url
client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")
# database connection
database = client[os.getenv("MONGO_DATABASE")]

text_data = database["text_data"]
sentiment_data = database["sentiment_data"]

text_data_db = database.get_collection("text_data")
sentiment_data_db = database.get_collection("sentiment_data")

# Create a function to get the subjectivity
def getSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity

# get all data
all_data_text = text_data_db.find({})

for data in all_data_text :
    # dict insert sentiment in mongo
    dict_sentiment = {}
    if 'text' in data:
        dict_sentiment["polarity"] = getPolarity(data["text"])
        dict_sentiment["subjectivity"] = getSubjectivity(data["text"])
        dict_sentiment["source"] = data["source"]
        dict_sentiment["date"] = data["date"]

        # if multpiple symbol associated text
        if isinstance(data["symbol"], list):
            for symbol in data["symbol"]:
                dict_sentiment["symbol"] = symbol
                dict_sentiment['_id'] = ObjectId() 
                sentiment_data_db.insert_one(dict_sentiment)

        else :
            dict_sentiment["symbol"] = data["symbol"]
            dict_sentiment['_id'] = ObjectId()
            sentiment_data_db.insert_one(dict_sentiment)


    # delete data in text_data_db
    text_data_db.delete_one({'text': data["text"]})

