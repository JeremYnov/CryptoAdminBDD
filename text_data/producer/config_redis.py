import base64
import redis


# connect to redis
client = redis.Redis(host="172.17.0.1", port=6379)


def create_key_value(key, value):
    # set a key
    client.set(key, base64.b64encode(value.encode()))


def get_value_by_key(keys):
    #   keys est une liste de clé
    #   return un dictionnaire clé et valeur
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
