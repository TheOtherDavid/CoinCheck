from datetime import datetime, timedelta
import cbpro


class CoinPriceDA:

    def get_price(self, currency):
        # Import cbpro classes
        # Get price for the given currency to USD.
        public_client = cbpro.PublicClient()
        currency_code = currency + "-USD"

        ticker_info = public_client.get_product_ticker(currency_code)
        price = ticker_info['price']

        #Should we persist the prices here, and return?

        return price
