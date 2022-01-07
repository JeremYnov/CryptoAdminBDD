
import redis


# connect to redis
client = redis.Redis(host='localhost', port=6379)

def create_key_value(key, value):
    # set a key
    client.set(key, value)

def get_value_by_key(key):
    # get a value
    value = client.get(key)
    # transform type value bytes -> str
    return value.decode("utf-8")