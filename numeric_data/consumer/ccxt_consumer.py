import os
from dotenv import load_dotenv
from json import loads
from pymongo import MongoClient
from kafka import KafkaConsumer

load_dotenv()


# get database url
mongo_url = "mongodb://{username}:{password}@mongodb:27017".format(
    username=os.getenv("MONGO_ROOT_USERNAME"), password=os.getenv("MONGO_ROOT_PASSWORD")
)
client = MongoClient(mongo_url)
# database connection
database = client[os.getenv("MONGO_DATABASE")]

# collections creation
numeric_data = database["numeric_data"]

# get collections
numeric_data_db = database.get_collection("numeric_data")


# Create Kafka consumer 
consumer = KafkaConsumer(
    "crypto_raw",
    bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVER")],
    api_version=(0, 10, 1),
)

for ccxt_raw in consumer:
    crypto = loads(ccxt_raw.value.decode("utf-8"))
    print(crypto)
    numeric_data_db.insert_one(
        {
            "date_time": crypto["datetime"],
            "price": crypto["last"],
            "symbol": crypto["symbol"],
            "high": crypto["high"],
            "low": crypto["low"],
            "average": crypto["average"],
        }
    )  
    # for n in numeric_data_db.find():
    #     print(n)
