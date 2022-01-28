import yfinance as yf
import streamlit as st
from PIL import Image
from urllib.request import urlopen
from datetime import date
from scripts.cmc_scraping import scrape
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

today = date.today()
min_date = date(2014, 10, 1)
load_dotenv()


def app():
    # mongoDB connexion
    client = MongoClient(
        "mongodb://{username}:{password}@mongodb:27017".format(
            username=os.getenv("MONGO_ROOT_USERNAME"),
            password=os.getenv("MONGO_ROOT_PASSWORD"),
        )
    )
    # database connexion
    database = client[os.getenv("MONGO_DATABASE")]
    # Get collections
    numerics_data_db = database.get_collection("numeric_data")
    sentiment_data_db = database.get_collection("sentiment_data")

    # Title
    st.title("Cryptocurrency Dashboard")

    # Defining ticker variable
    Bitcoin = "BTC-USD"

    # Access data from Yahoo Finance
    BTC_Data = yf.Ticker(Bitcoin)

    # Fetch history data from Yahoo Finance
    BTCHis = BTC_Data.history(period="max")

    # Creation of 2 columns (like display flex for web)
    col1, col2 = st.columns((1, 5))
    col2.header("BITCOIN ($)")
    # Display image
    imageBTC = Image.open(
        urlopen("https://s2.coinmarketcap.com/static/img/coins/64x64/1.png")
    )
    col1.image(imageBTC, use_column_width=False)
    # Calendar to choose a date
    date = st.date_input(
        "Choose a date",
        value=today,
        min_value=min_date,
        max_value=today,
        disabled=False,
    )

    # Fetch crypto data for the dataframe
    st.subheader("From yahoo finance")
    BTC = yf.download(Bitcoin, start=date, end=date)
    # Display dataframe
    st.table(BTC)

    # Fetch crypto data for the dataframe
    st.subheader("From Coin Market Cap Scraping")
    # Get date and transform in string for scrape function
    date_time = date.strftime("%Y%m%d")
    # Launch scrape function to get scraped data from CMC
    scraped_data = scrape(date_time)
    # Check if scraped_data is not empty
    if scraped_data:
        for crypto in scraped_data:
            # Take only data from Bitcoin
            if crypto["Name"] == "Bitcoin":
                # Add data on df for display on st.table
                crypto_df = pd.DataFrame(crypto, index=[0])
                # Create the table
                st.table(crypto_df)
                break
    else:
        st.subheader("No data to display")

    st.header("Daily Prices")
    # Display a chart daily prices
    st.bar_chart(BTCHis.Close)

    # Get all symbols without doublon
    symbols = numerics_data_db.find({"symbol": {"$regex": "BTC/"}}).distinct("symbol")
    st.header("Real Time Price")
    # Get real time price from ccxt API
    for symbol in symbols:
        data_by_symbol = (
            numerics_data_db.find({"symbol": symbol}, {"_id": False})
            .limit(1)
            .sort("$natural", -1)
        )
        for data in data_by_symbol:
            data_by_symbol_df = pd.DataFrame(data, index=[0])
            st.write(data_by_symbol_df)
     
    st.header("Sentiment Analysis")       
    # Get sentiment analysis avg 
    # Needed by interface to say if the sentiments ar good or bad
    avg_sentiments = sentiment_data_db.aggregate(
        [
            {
                "$group": {
                    "_id": "$symbol",
                    "avgPolarity": {"$avg": "$polarity"},
                    "avgSubjectivity": {"$avg": "$subjectivity"},
                }
            }
        ]
    )
    count_sentiment = sentiment_data_db.find({"symbol": "BTC"}).count()
    # Get only sentiment avg for the page symbol
    st.write('Polarity is float which lies in the range of [-1,1] where 1 means positive statement and -1 means a negative statement. Subjective sentences generally refer to personal opinion, emotion or judgment whereas objective refers to factual information. Subjectivity is also a float which lies in the range of [0,1].')
    st.write("nb d'analyse " + str(count_sentiment))
    for avg_sentiment_by_symbol in avg_sentiments:
        if avg_sentiment_by_symbol["_id"] == "BTC":
            col1, col2 = st.columns(2)
            col1.metric("","Polarity", round(avg_sentiment_by_symbol['avgPolarity'],2))
            col2.metric("","Subjectivity", round(avg_sentiment_by_symbol['avgSubjectivity'], 2))