import os
from dotenv import load_dotenv
from pymongo import MongoClient
from kafka import KafkaConsumer
from json import loads
from datetime import datetime

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

    # arborescence crypto = {
    # "redit": [{"subreddit": "BTC", "title": "title"},{"subreddit": "BTC", "title": "text"}]},
    # "data_twitter": [{"Tweet": "text", "Symbol": "BTC"},{"Tweet": "text", "Symbol": "BTC"}]},
    # "cryptopanic": [{"title": "text", "code": "BTC"},{"title": "text", "code": "BTC"}]}

    # insert data redit
    for redit in crypto["redit"]:
        # if data not in collection -> insert
        if not text_data_db.find_one({"text": redit["title"]}):
            text_data_db.insert_one({
                "symbol" : redit["subreddit"],
                "text" : redit["title"],
                "source" : "redit",
                "date": datetime.now().strftime('%d-%m-%Y')
                }
            )
    
    for twitter in crypto["data_twitter"]:
        # if data not in collection -> insert
        if not text_data_db.find_one({"text": twitter["Tweet"]}):
            text_data_db.insert_one({
                "symbol" : twitter["Symbol"],
                "text" : twitter["Tweet"],
                "source" : "twitter",
                "date": datetime.now().strftime('%d-%m-%Y')
                }
            )

    for new in crypto["cryptopanic"]:
        # dictionnaire insert in mongo
        dict_cryptopanic = {}
        # if symbol exists in dict
        if 'currencies' in new:
            # if data not in collection -> insert
            if not text_data_db.find_one({"text": new["title"]}):
                # insert in dict title
                dict_cryptopanic["text"] = new["title"]
                # list contains symbols
                list_symbol = []
                # for in symbols
                for code in new["currencies"] :
                    if code["code"] == "BTC" or code["code"] == "ETH" or code["code"] == "SOL":
                        list_symbol.append(code["code"])
                # insert in dict list symbol associeted title
                dict_cryptopanic["symbol"] = list_symbol
                dict_cryptopanic["source"] = "cryptopanic"
                dict_cryptopanic["date"] = datetime.now().strftime('%d-%m-%Y')
                # insert in mongodb
                text_data_db.insert_one(dict_cryptopanic)
    
    
    
    for n in text_data_db.find():
        print(n)
