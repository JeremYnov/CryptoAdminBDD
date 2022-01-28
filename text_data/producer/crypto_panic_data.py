import os
import requests
from dotenv import load_dotenv
from config_redis import get_value_by_key, var_crypto_panic

def get_data_crypto_panic():
    """
    get cryptopanic data
    return [list dict]
    """
    load_dotenv()
    key = get_value_by_key(var_crypto_panic)
    url = "{url}?auth_token={token}&currencies=BTC,ETH,SOL".format(url=os.getenv('CRYPTO_PANIC_API_URL'),
                                        token=key["CRYPTO_PANIC_API_KEY"])
    page = requests.get(url)
    data = page.json()
    news = data["results"]
    return news

get_data_crypto_panic()
