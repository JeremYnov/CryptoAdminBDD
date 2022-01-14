import pandas as pd
import requests
from bs4 import BeautifulSoup

# Create empty list to store the data
crypto_name_list = []
crypto_market_cap_list = []
crypto_price_list = []
crypto_circulating_supply_list = []
crypto_symbol_list = []

# Create an empty dataframe to organize data
df = pd.DataFrame()


def scrape(date="20211219/"):
    # Get the website URL we want to scrape
    URL = "https://coinmarketcap.com/historical/" + date
    # Make a request to the website
    webpage = requests.get(URL)
    # Parse text from website
    soup = BeautifulSoup(webpage.text, "html.parser")
    # Get the table row element
    tr = soup.find_all("tr", attrs={"class": "cmc-table-row"})
    # Create a count variable for the number of crypto we want to scrape
    count = 0
    # Loop through every row to gather the data
    for row in tr:
        # if the count is reached then break out
        if count == 10:
            break
        count = count + 1  # increment cont by 1

        # Store cryptocurency name in variable
        # Find the td element to later get the crypto name
        name_column = row.find(
            "td",
            attrs={
                "class": "cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name"
            },
        )
        crypto_name = name_column.find(
            "a", attrs={"class": "cmc-table__column-name--name cmc-link"}
        )
        # Store the cryptocurrency coin market cap
        crypto_market_cap = row.find(
            "td",
            attrs={
                "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap"
            },
        ).text.strip()
        # Find and store the crypto price
        crypto_price = row.find(
            "td",
            attrs={
                "class": "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"
            },
        ).text.strip()
        # Find and store the crypto supply and symbol
        crypto_circulating_supply_and_symbol = row.find(
            "td",
            attrs={
                "class": "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply"
            },
        ).text.strip()
        # Split data
        crypto_circulating_supply = crypto_circulating_supply_and_symbol.split(" ")[0]
        crypto_symbol = crypto_circulating_supply_and_symbol.split(" ")[1]

        # Append the data to list
        crypto_name_list.append(crypto_name)
        crypto_market_cap_list.append(crypto_market_cap)
        crypto_price_list.append(crypto_price)
        crypto_circulating_supply_list.append(crypto_circulating_supply)
        crypto_symbol_list.append(crypto_symbol)


# Run the scrape function
scrape(date="20211219/")
print(crypto_name_list)
# Store data into df
# df["Name"] = crypto_name_list           
# df["Symbol"] = crypto_symbol_list
# df["Market Cap"] = crypto_market_cap_list
# df["Price"] = crypto_price_list
# df["Cicrulating Supply"] = crypto_circulating_supply_list

print(df)
