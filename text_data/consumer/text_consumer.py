import os
from dotenv import load_dotenv
from pymongo import MongoClient
from kafka import KafkaConsumer
from json import loads

load_dotenv()

# connexion à la bdd
mongo_url = "mongodb://{username}:{password}@mongodb:27017".format(
    username=os.getenv("MONGO_ROOT_USERNAME"), password=os.getenv("MONGO_ROOT_PASSWORD")
)
client = MongoClient(mongo_url)

# connexion à la database
database = client[os.getenv("MONGO_DATABASE")]


consumer = KafkaConsumer(
    "text", bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVER")]
)

# on balaye la liste news qui contient les news pour garder seulement les news qui ont un "code" crypto
for new in consumer:
    crypto = loads(new.value.decode("utf-8"))
    # print(crypto)
