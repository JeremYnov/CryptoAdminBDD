import os
import requests
from dotenv import load_dotenv
from json import dumps
from kafka import KafkaProducer
from time import sleep
from cryptoPanicData import get_data_crypto_panic
from redditData import get_data_reddit
from twitterData import get_data_twitter

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)


while True:
    try:
        # data_crypto_panic = get_data_crypto_panic()
        data_redit = get_data_reddit()
        data_twitter = get_data_twitter()

        dict_data= {
            # "cryptopanic" : data_crypto_panic,
            "redit": data_redit,
            "data_twitter": data_twitter
        }

        producer.send("text", dict_data)
    except:
        print("error")
    sleep(60)
