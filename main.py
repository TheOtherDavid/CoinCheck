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

    # Get last six hours prices
    price_records = priceStorageDA.getPrices(product_code)["Items"]
    current_price_record = price_records[0]
    current_price = float(current_price_record["PRC"])


    price_date_string = None
    percentage_difference = None
    send_message = False

    alert_target_difference = float(os.environ.get("alert_target_difference"))

    # Compare the current price to the previous prices
    for price_record in price_records:
        # Technically this compares current_price to itself the first time around the loop, but it shouldn't matter.
        price = float(price_record["PRC"])
        price_date = datetime.strptime(price_record["DTM"], "%Y-%m-%d %H:%M:%S.%f%z")
        price_date_string = datetime.strftime(price_date, "%H:%M:%S")
        percentage_difference = (current_price - price) / abs(price) * 100
        percentage_difference = round(percentage_difference, 2)
        if abs(percentage_difference > alert_target_difference):
            # The FIRST TIME that the price has a >X% difference, break that loop
            send_message = True
            break

    # Send SMS message
    if send_message:
        messageDA = MessageDA()
        env = os.getenv("env")
        # Adding newline to beginning of the message to avoid sending blank text because of colon character.
        message = "\nGreetings from " + str(env) + ". " + \
                  str(product_code) + " is currently at " + str(price) + \
                  ". This is a change of " + str(percentage_difference) + "% since " + \
                  price_date_string + "."

        messageDA.send_message(message)


if __name__ == '__main__':
    handler(None, None)
