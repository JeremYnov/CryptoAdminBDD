import ccxt
import os
from dotenv import load_dotenv
from json import dumps
from kafka import KafkaProducer
from time import sleep

load_dotenv()

# Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"),
#     value_serializer=lambda x: dumps(x).encode("utf-8"),
# )

# Get binance market data
binance = ccxt.binanceus()

# Get crypto-currencies data every 20sec and send them on producer
while True:
    try:
        # Get all crypto-currencies from binance
        tickers = binance.fetch_tickers()
        # Loop on crypto-currencies
        for ticker in tickers.values():
            # Get crypto-currencies symbol (ex: "BTC", "ETH"...)
            ticker_symbol = ticker["symbol"].split("/")[0]
            # Condition to get only the crypto-currencies we are interested in
            if (
                ticker_symbol == "BTC"
                or ticker_symbol == "ETH"
                or ticker_symbol == "SOL"
            ):
                print(ticker)
                # Send data with kafka producer
                # producer.send("crypto_raw", ticker)
    except:
        print("ooops")
    sleep(20)
