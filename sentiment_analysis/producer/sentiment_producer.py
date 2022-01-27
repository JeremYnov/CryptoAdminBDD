import ccxt
import os
from dotenv import load_dotenv
from json import dumps
from kafka import KafkaProducer
from time import sleep
from pymongo import MongoClient


load_dotenv()

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)

# Get binance market data
binance = ccxt.binanceus()

# Get crypto-currencies data every 20sec and send them on producer
while True:
    try:
        client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")
        # database connection
        database = client[os.getenv("MONGO_DATABASE")]

        text_data = database["text_data"]
        text_data_db = database.get_collection("text_data")
        list_text_data_db = []
        for data in text_data_db.find({}, {'_id': 0}) :
            list_text_data_db.append(data)
        dict_data = {"data" : list_text_data_db}
        producer.send("sentiment", dict_data)
    except:
        print("ooops")
    sleep(20)