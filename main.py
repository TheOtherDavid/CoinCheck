# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from MessageDA import MessageDA
from CoinPriceDA import CoinPriceDA


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def handler(event, context):
    print_hi('PyCharm')
    # Get price from Coinbase
    coinPriceDA = CoinPriceDA()
    price = coinPriceDA.get_price("BTC")

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
        messageDA.send_message("BTC is currently at " + price)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler(None, None)
