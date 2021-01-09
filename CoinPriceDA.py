from datetime import datetime, timedelta
import cbpro


class CoinPriceDA:

    def get_price(self, currency):
        # Import cbpro classes
        # Get price for the given currency to USD.
        public_client = cbpro.PublicClient()
        currency_code = currency + "-USD"

        price = public_client.get_product_ticker(currency_code)

        #Should we persist the prices here, and return?

        #Return prices.
