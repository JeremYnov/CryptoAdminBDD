import ccxt
import os
from dotenv import load_dotenv
from json import dumps
from kafka import KafkaProducer
from time import sleep
from pymongo import MongoClient
from function_sentiment import getPolarity, getSubjectivity, write_csv_text_data
from bson.objectid import ObjectId


load_dotenv()

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)


# Get crypto-currencies data every 20sec and send them on producer
while True:
    try:
        client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")
        # database connection
        database = client[os.getenv("MONGO_DATABASE")]

        text_data = database["text_data"]
        text_data_db = database.get_collection("text_data")
        sentiment_data = database["sentiment_data"]
        sentiment_data_db = database.get_collection("sentiment_data")

        # list send on csv send on hadoop
        list_text_data_hadoop = []
        for data in text_data_db.find({}, {'_id': 0}):
            
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
            print(data)
            if 'text' in data:
                # delete data in text_data_db
                text_data_db.delete_one({'text': data["text"]})
        # write csv (text data) for hadoop
        write_csv_text_data(list_text_data_hadoop)

        print("text_data restant")
        print(text_data_db.find().count())
        print("sentiment data")  
        print(sentiment_data_db.find().count())

        producer.send("sentiment", data)
    except:
        print("ooops")
    sleep(3600)