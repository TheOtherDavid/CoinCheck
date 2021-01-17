from datetime import datetime, timedelta
import cbpro


class CoinPriceDA:

    def get_price(self, product):
        # Import cbpro classes
        # Get price for the given currency to USD.
        public_client = cbpro.PublicClient()

        ticker_info = public_client.get_product_ticker(product)
        price = ticker_info['price']

        # Should we persist the prices here, and return?

        return price
