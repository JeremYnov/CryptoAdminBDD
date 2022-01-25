import os
from dotenv import load_dotenv
from pymongo import MongoClient
from kafka import KafkaConsumer
from json import loads

load_dotenv()

# get database url
client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")
# database connection
database = client[os.getenv("MONGO_DATABASE")]

# collections creation
text_data = database["text_data"]

# get collections
text_data_db = database.get_collection("text_data")
text_data_db.create_index('text')


consumer = KafkaConsumer(
    "text", bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVER")]
)

# on balaye la liste news qui contient les news pour garder seulement les news qui ont un "code" crypto
for new in consumer:
    crypto = loads(new.value.decode("utf-8"))
    # insert data redit
    for redit in crypto["redit"]:
        if not text_data_db.find_one({"text": redit["title"]}):
            text_data_db.insert_one({
                "symbol" : redit["subreddit"],
                "text" : redit["title"],
                "source" : "redit"
                }
            )
    
    for redit in crypto["data_twitter"]:
        if not text_data_db.find_one({"text": redit["Tweet"]}):
            text_data_db.insert_one({
                "symbol" : redit["Symbol"],
                "text" : redit["Tweet"],
                "source" : "twitter"
                }
            )
    
    for n in text_data_db.find():
        print(n)
