import base64
import os
import redis
from dotenv import load_dotenv

load_dotenv()

# connect to redis
client = redis.Redis(host="127.0.0.1", port=6379)


def create_key_value(key, value):
    # set a key
    client.set(key, base64.b64encode(value.encode()))

# insert token twitter
create_key_value("TWITTER_CONSUMER_KEY", os.getenv('TWITTER_CONSUMER_KEY'))
create_key_value("TWITTER_CONSUMER_SECRET", os.getenv('TWITTER_CONSUMER_SECRET'))
create_key_value("TWITTER_ACCESS_TOKEN", os.getenv('TWITTER_ACCESS_TOKEN'))
create_key_value("TWITTER_ACCESS_TOKEN_SECRET", os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

# insert token crypto panic
create_key_value("CRYPTO_PANIC_API_KEY", os.getenv('CRYPTO_PANIC_API_KEY'))

# insert token reddit
create_key_value("REDDIT_CLIENT_ID", os.getenv('REDDIT_CLIENT_ID'))
create_key_value("REDDIT_SECRET_TOKEN", os.getenv('REDDIT_SECRET_TOKEN'))


