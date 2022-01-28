# import pandas as pd
import requests
from bs4 import BeautifulSoup

# Create empty list to store the data

crypto_list = []

# This function is use to scrape data from coin market cap
# we must give it as a parameter the date of the day we want to scrape the data
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
    crypto_count = 0
    # Loop through every row to gather the data
    for row in tr:
        # # if the count is reached then break out
        if crypto_count == 10:
            break
        crypto_count += 1  # increment count by 1

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

        if (
            crypto_name.text == "Bitcoin"
            or crypto_name.text == "Ethereum"
            or crypto_name.text == "Solana"
            and count < 4
        ):
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
            crypto_circulating_supply = crypto_circulating_supply_and_symbol.split(" ")[
                0
            ]
            crypto_symbol = crypto_circulating_supply_and_symbol.split(" ")[1]

            # Store scrapping data in JSON format
            crypto_list.append(
                {
                    "Name": crypto_name.text,
                    "Symbol": crypto_symbol,
                    "Market Cap": crypto_market_cap,
                    "Price": crypto_price,
                    "Circulating Supply": crypto_circulating_supply,
                }
            )
            count += 1
    return crypto_list


# Run the scrape function
scrapped_data = scrape(date="20211219/")
print(scrapped_data)
