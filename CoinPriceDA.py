from datetime import datetime, timedelta
import os
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

    def get_account_balances(self):
        key = os.getenv("cbpro_key")
        secret = os.getenv("cbpro_secret")
        passphrase = os.getenv("cbpro_passphrase")

        authenticated_client = cbpro.AuthenticatedClient(key, secret, passphrase)
        balance_records = authenticated_client.get_accounts()
        filtered_balance_records = []
        for balance_record in balance_records:
            if float(balance_record["balance"]) != 0:
                filtered_balance_records.append(balance_record)

        return filtered_balance_records
