import yfinance as yf
import streamlit as st
from PIL import Image
from urllib.request import urlopen
from datetime import date
from scripts.cmc_scraping import scrape
import pandas as pd

today = date.today()
min_date = date(2014, 10, 1)


def app():
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
