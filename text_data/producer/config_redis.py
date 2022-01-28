import base64
import redis

# connect to redis
client = redis.Redis(host="172.17.0.1", port=6379)


def create_key_value(key, value):
    """insert in base redis
    args :
        key [str] : key associated value
        value [str] : value of credential
    """

    client.set(key, base64.b64encode(value.encode()))


def get_value_by_key(keys):
    """  get value by key in base redis
    args :
        keys [list] : list of different key
    return [dict] : dict of credential
    """
    dico = {}
    for key in keys:
        value = client.get(key)
        dico[key] = base64.b64decode(value).decode("utf-8")
    return dico


var_env = [
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
]

var_crypto_panic = ["CRYPTO_PANIC_API_KEY"]

var_reddit = ["REDDIT_CLIENT_ID", "REDDIT_SECRET_TOKEN"]


