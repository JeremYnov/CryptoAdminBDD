import os
import requests
from dotenv import load_dotenv

# from json import dumps
# from kafka import KafkaProducer
from time import sleep

load_dotenv()

# producer = KafkaProducer(
#     bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"),
#     value_serializer=lambda x: dumps(x).encode("utf-8"),
# )

url = "{url}?auth_token={token}&currencies=BTC,ETH,SOL".format(
    url=os.getenv("CRYPTO_PANIC_API_URL"), token=os.getenv("CRYPTO_PANIC_API_KEY")
)
print(url)

while True:
    try:
        page = requests.get(url)
        data = page.json()
        news = data["results"]
        for new in news:
            if 'currencies' in new:
                print(new['currencies'])
        # producer.send("crypto_news", news)
    except:
        print("error")
    sleep(20)
