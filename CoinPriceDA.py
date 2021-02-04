import os
import cbpro


class CoinPriceDA:

    def get_price(self, product_id):
        # Import cbpro classes
        # Get price for the given currency to USD.
        public_client = cbpro.PublicClient()

        ticker_info = public_client.get_product_ticker(product_id)
        price = ticker_info['price']

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

    def get_orders(self, product_id):
        key = os.getenv("cbpro_key")
        secret = os.getenv("cbpro_secret")
        passphrase = os.getenv("cbpro_passphrase")

        authenticated_client = cbpro.AuthenticatedClient(key, secret, passphrase)
        orders_gen = authenticated_client.get_orders(product_id=product_id, status='done')
        order_records = list(orders_gen)

        # Not all orders include price. Enrich orders with price.
        for order in order_records:
            value = float(order["executed_value"])
            quantity = float(order["filled_size"])
            price = value / quantity
            #Adjust orders with negative quantity for sells
            if order["side"] == "sell":
                quantity = -quantity
            order["price"] = price
            order["quantity"] = quantity

        return order_records