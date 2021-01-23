import os
import pytz

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
    eastern = pytz.timezone('US/Eastern')
    time = datetime.now(eastern)
    priceStorageDA.savePrice(time, product_code, price)

    # Get all prices (maybe last six hours?)
    rows = priceStorageDA.getPrices(product_code)["Items"]
    current_price_record = rows[0]
    current_price = float(current_price_record["PRC"])
    last_price_record = rows[1]
    last_price = float(last_price_record["PRC"])
    last_price_date = datetime.strptime(last_price_record["DTM"], "%Y-%m-%d %H:%M:%S.%f%z")
    last_price_date_string = datetime.strftime(last_price_date, "%H:%M:%S")
    percentage_difference = (current_price - last_price) / abs(last_price) * 100
    percentage_difference = round(percentage_difference, 2)

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
        # Adding newline to beginning of the message to avoid sending blank text because of colon character.
        message = "\nGreetings from " + str(env) + ". " + \
                  str(product_code) + " is currently at " + str(price) + \
                  ". This is a change of " + str(percentage_difference) + "% since " + \
                  last_price_date_string + "."

        messageDA.send_message(message)


if __name__ == '__main__':
    handler(None, None)
