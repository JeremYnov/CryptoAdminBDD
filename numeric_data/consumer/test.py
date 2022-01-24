import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

# get database url
client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")

# database connection
database = client[os.getenv("MONGO_DATABASE")]

# collections creation
numeric_data = database["numeric_da"]
print(numeric_data)

# get collections
numeric_data_db = database.get_collection("numeric_da")
for n in numeric_data_db.find({}):
    print(n)