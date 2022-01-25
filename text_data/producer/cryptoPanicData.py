import os
import requests
from dotenv import load_dotenv



def get_data_crypto_panic():
    load_dotenv()
    url = "{url}?auth_token={token}&currencies=BTC,ETH,SOL".format(url=os.getenv('CRYPTO_PANIC_API_URL'),
                                        token=os.getenv('CRYPTO_PANIC_API_KEY'))
    page = requests.get(url)
    data = page.json()
    news = data["results"]
    return news

get_data_crypto_panic()


