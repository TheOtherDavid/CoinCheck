import os
import pytz

from datetime import datetime

from MessageDA import MessageDA
from CoinPriceDA import CoinPriceDA
from PriceStorageDA import PriceStorageDA


def handler(event, context):
    # Setting a single start time.
    eastern = pytz.timezone('US/Eastern')
    start_time = datetime.now(eastern)

    # We have to record balances before the price alert, because it now depends on balances.
    record_balances(start_time)
    price_alert(start_time)

    # plot_balances()

def plot_balances():
    # TODO: This is a bandaid to avoid errors with the import layer.
    from GraphDA import GraphDA

    priceStorageDA = PriceStorageDA()
    balance_records = priceStorageDA.getBalances()
    graphDA = GraphDA()
    graphDA.plot_data(balance_records)


def record_balances(start_time):
    coinPriceDA = CoinPriceDA()
    balance_records = coinPriceDA.get_account_balances()

    for balance_record in balance_records:

        balance_record["time"] = start_time
        product = balance_record["currency"]
        if product != "USD":
            product_code = balance_record["currency"]
            balance_record["price"] = coinPriceDA.get_price(product_code)
            order_records = coinPriceDA.get_orders(product_code)

            total_quantity = 0
            total_value = 0

            for order_record in order_records:
                quantity = order_record["quantity"]
                price = order_record["price"]
                value = quantity * price
                total_quantity = total_quantity + quantity
                total_value = total_value + value

            if total_quantity != 0:
                average_price = total_value / total_quantity
            else:
                average_price = 0
            balance_record["average_price"] = average_price

        if product == "USD":
            balance_record["price"] = 1
            balance_record["average_price"] = 1
        priceStorageDA = PriceStorageDA()
        priceStorageDA.saveBalance(balance_record)
    print(f"Balances recorded")


def price_alert(start_time):
    product_codes = ["BTC", "ETH"]


    for product_code in product_codes:
        # Get price from Coinbase
        coinPriceDA = CoinPriceDA()
        price = coinPriceDA.get_price(product_code)

        # Store price in DB
        priceStorageDA = PriceStorageDA()

        env = os.getenv("env")
        priceStorageDA.savePrice(start_time, product_code, price)

        # Get last six hours prices
        price_records = priceStorageDA.getPrices(start_time, product_code)
        current_price_record = price_records[0]
        current_price = float(current_price_record["PRC"])
        print(f"Current price for " + product_code + " is " + str(current_price))

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
            if abs(percentage_difference) > alert_target_difference:
                # The FIRST TIME that the price has a >X% difference, break that loop
                send_message = True
                break
        print(f"Largest percent difference for " + product_code + ": " + str(percentage_difference))

        # Send SMS message
        if send_message:
            # Get the current data for this product
            current_balance_record = priceStorageDA.get_current_balance(start_time, product_code)
            average_price = round(current_balance_record["AVG_PRC"], 2)
            percentage_gain = round((current_price - average_price) / average_price * 100, 2)
            messageDA = MessageDA()
            print(f"Sending message.")
            # Adding newline to beginning of the message to avoid sending blank text because of colon character.
            message = "\nGreetings from " + str(env) + ". " + \
                      str(product_code) + " is currently at " + str(price) + \
                      ". This is a change of " + str(percentage_difference) + "% since " + \
                      price_date_string + ". Your average purchase price was " + str(average_price) + \
                      " and your profit is " + str(percentage_gain) + "."

            messageDA.send_message(message)

if __name__ == '__main__':
    handler(None, None)
