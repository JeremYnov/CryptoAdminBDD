import os
import requests
from dotenv import load_dotenv



def get_data_crypto_panic():
    load_dotenv()
    url = "{url}?auth_token={token}".format(url=os.getenv('CRYPTO_PANIC_API_URL'),
                                        token=os.getenv('CRYPTO_PANIC_API_KEY'))

    page = requests.get(url)
    data = page.json()
    news = data["results"]
    return news
    # for new in news:
    #     if 'currencies' in new:
    #         print(new["title"])

get_data_crypto_panic()

