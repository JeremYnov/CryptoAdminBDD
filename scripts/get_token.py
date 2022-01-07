import base64
from config_redis import get_value_by_key

# on recupere les tokens a l'aide de leur clé
twitterConsumerKey = get_value_by_key("twitterConsumerKey")
twitterConsumerSecret = get_value_by_key("twitterConsumerSecret")
twitterAccessToken = get_value_by_key("twitterAccessToken")
twitterAccessTokenSecret = get_value_by_key("twitterAccessTokenSecret")

# on decrypte les tokens en str
twitterConsumerKey = base64.b64decode(twitterConsumerKey).decode("utf-8")
print(twitterConsumerKey)

twitterConsumerSecret = base64.b64decode(twitterConsumerSecret).decode("utf-8")
print(twitterConsumerSecret)

twitterAccessToken = base64.b64decode(twitterAccessToken).decode("utf-8")
print(twitterAccessToken)

twitterAccessTokenSecret = base64.b64decode(twitterAccessTokenSecret).decode("utf-8")
print(twitterAccessTokenSecret)



