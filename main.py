import os
import pytz

from datetime import datetime
from MessageDA import MessageDA
from CoinPriceDA import CoinPriceDA
from PriceStorageDA import PriceStorageDA


def handler(event, context):
    env = os.getenv("env")
    #TODO: Remove this later? Currently a hack to prevent AWS from erroring because I haven't updated the layer.
    if env == 'AWS':
        record_balances()
        price_alert()
    else:
        plot_balances()

def plot_balances():
    #TODO: Move import up higher once you update the layer with pandas and pyplot
    from GraphDA import GraphDA

    priceStorageDA = PriceStorageDA()
    balance_records = priceStorageDA.getBalances()
    graphDA = GraphDA()
    graphDA.plot_data(balance_records)


def record_balances():
    coinPriceDA = CoinPriceDA()
    balance_records = coinPriceDA.get_account_balances()

    eastern = pytz.timezone('US/Eastern')
    time = datetime.now(eastern)

    for balance_record in balance_records:

        balance_record["time"] = time
        product = balance_record["currency"]
        if product != "USD":
            product_code = balance_record["currency"] + "-USD"
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


def price_alert():
    product_codes = ["BTC-USD", "ETH-USD"]

    for product_code in product_codes:
        # Get price from Coinbase
        coinPriceDA = CoinPriceDA()
        price = coinPriceDA.get_price(product_code)

        # Store price in DB
        priceStorageDA = PriceStorageDA()
        eastern = pytz.timezone('US/Eastern')
        time = datetime.now(eastern)
        env = os.getenv("env")
        priceStorageDA.savePrice(time, product_code, price)

        # Get last six hours prices
        price_records = priceStorageDA.getPrices(product_code)["Items"]
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
            messageDA = MessageDA()
            print(f"Sending message.")
            # Adding newline to beginning of the message to avoid sending blank text because of colon character.
            message = "\nGreetings from " + str(env) + ". " + \
                      str(product_code) + " is currently at " + str(price) + \
                      ". This is a change of " + str(percentage_difference) + "% since " + \
                      price_date_string + "."

            messageDA.send_message(message)

if __name__ == '__main__':
    handler(None, None)
