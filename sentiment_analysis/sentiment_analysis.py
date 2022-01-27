import os
from dotenv import load_dotenv
from pymongo import MongoClient
from textblob import TextBlob
from bson.objectid import ObjectId
import csv
import glob


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

def write_csv_text_data(list_text_data_hadoop):
    """write csv for hadoop"""
    # create folder csv if nos exists
    final_directory = os.path.join(os.getcwd(), 'csv')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    # get the last csv for get file number data
    last_csv = glob.glob(f"{final_directory}/*")
    # get number
    if last_csv == [] :
        number_last_csv = 0
    else :
        number_last_csv = last_csv[-1].split("/")[-1].split(".")[0].split("data")[-1]

    # path csv create
    path = f'{final_directory}/data{int(number_last_csv) + 1}.csv'

    # write data text in csv
    if list_text_data_hadoop != []:
        keys = list_text_data_hadoop[0].keys()
        with open(path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list_text_data_hadoop)
    


# print("Text")
# for t in text_data_db.find({}):
#         print(t)
# print("no text")
# for t in text_data_db.find({}):
#     if 'text' not in t:
#         print(t)

# # get all data
all_data_text = text_data_db.find({})
# list send on csv send on hadoop
list_text_data_hadoop = []

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
    # list send on csv send on hadoop
    list_text_data_hadoop.append(data)
    

    if 'text' in data:
        # delete data in text_data_db
        text_data_db.delete_one({'text': data["text"]})

# write csv (text data) for hadoop
write_csv_text_data(list_text_data_hadoop)



print(sentiment_data_db.find().count())


