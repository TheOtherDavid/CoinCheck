from datetime import datetime
from MessageDA import MessageDA
from CoinPriceDA import CoinPriceDA
from PriceStorageDA import PriceStorageDA


def handler(event, context):
    product_code = "BTC-USD"
    # Get price from Coinbase
    coinPriceDA = CoinPriceDA()
    price = coinPriceDA.get_price(product_code)

    priceStorageDA = PriceStorageDA()
    time = datetime.now(None)
    priceStorageDA.savePrice(time, product_code, price)

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
        messageDA.send_message(product_code + " is currently at " + price)


if __name__ == '__main__':
    handler(None, None)
