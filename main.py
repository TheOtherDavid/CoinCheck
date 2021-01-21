import os
from datetime import datetime
from MessageDA import MessageDA
from CoinPriceDA import CoinPriceDA
from PriceStorageDA import PriceStorageDA


def handler(event, context):
    product_code = "BTC-USD"
    # Get price from Coinbase
    coinPriceDA = CoinPriceDA()
    price = coinPriceDA.get_price(product_code)

    # Store price in DB
    priceStorageDA = PriceStorageDA()
    time = datetime.now(None)
    priceStorageDA.savePrice(time, product_code, price)

    # Get all prices (maybe last six hours?)
    rows = priceStorageDA.getPrices(product_code)

    # Do logic on that price
    # Store the price, retrieve the previous prices, and do math on it?
    # I guess I need a DB.

    # Compare the current price to, in order:
    # The price from 1 hour, 2 hour, 3 hours, 4 hours, 5 hours, and 6 hours ago.
    # The FIRST TIME that the price has a >10% difference, break that loop
    # Report that the prices have risen/dropped the amount in the time amount.

    # Send SMS message
    if True:
        messageDA = MessageDA()
        env = os.getenv("env")
        message = "Greetings from " + env + ". " + \
                  product_code + " is currently at " + str(price)
        messageDA.send_message(message)


if __name__ == '__main__':
    handler(None, None)
