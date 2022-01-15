CLIENT_ID = "LlZQ0PdhzZokLLhHA56avw"
SECRET_TOKEN = "7HFRAddxFtsfw4Rx_vt8lz0A4katxQ"

import requests
import pandas as pd

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

# here we pass our login method (password), username, and password
data = {"grant_type": "password", "username": "Baloord", "password": "Devaccount2022"}

# setup our header info, which gives reddit a brief description of our app
headers = {"User-Agent": "MyBot/0.0.1"}

# send our request for an OAuth token
res = requests.post(
    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers
)

# convert response to JSON and pull access_token value
TOKEN = res.json()["access_token"]

# add authorization to our headers dictionary
headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

# make a request for the trending posts in /r/Python
res = requests.get("https://oauth.reddit.com/r/bitcoin/hot", headers=headers)

df = pd.DataFrame()  # initialize dataframe

# loop through each post retrieved from GET request
for post in res.json()["data"]["children"]:
    # append relevant data to dataframe
    df = df.append(
        {
            "subreddit": post["data"]["subreddit"],
            "title": post["data"]["title"],
            "selftext": post["data"]["selftext"],
            "upvote_ratio": post["data"]["upvote_ratio"],
            "ups": post["data"]["ups"],
            "downs": post["data"]["downs"],
            "score": post["data"]["score"],
        },
        ignore_index=True,
    )
    print(df)
