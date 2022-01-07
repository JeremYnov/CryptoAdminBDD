import ccxt 
import time 

binance = ccxt.binanceus()

while True:
  try:
    tickers = binance.fetch_tickers()

    for ticker in tickers.values():
        print(ticker)
        #   producer.send('crypto_raw', ticker)
  except:
    print('ooops')

  time.sleep(20)