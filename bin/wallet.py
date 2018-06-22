from datetime import datetime


class Wallet:
    def __init__(self):
        self.value = 0
        self.market_value = 0
        self.shares_history = []
        self.wallet = {}

    def add_funds(self, amount):
        self.value += amount

    def remove_funds(self, amount):
        self.add_funds(-amount)

    def register_transaction(self, transaction_type, stock, quantity, price):  # Negative quantity means sale
        transaction_value = quantity * price
        transaction_time = datetime.now()

        self.shares_history.append([transaction_type, stock, abs(quantity), price, abs(transaction_value), transaction_time])

        self.market_value += transaction_value  # Add transaction value to market value

        try:  # Try to update values in dictionary
            self.wallet[stock]["Quantity"] += quantity
            self.wallet[stock]["MarketValue"] += transaction_value
            self.wallet[stock]["Price"] = self.wallet[stock]["MarketValue"] / self.wallet[stock]["Quantity"]

        except KeyError:
            self.wallet[stock] = {"Quantity": quantity, "Price": price, "MarketValue": transaction_value}

        with open("wallet.log.out", "a") as wallet_log:
            wallet_log.write('{0} {1} {2} {3} {4}\n'.format(transaction_type, stock, quantity, price, transaction_value))

    def register_dividend(self, amount_per_share, stock):
        quantity = self.shares[stock][1]

        self.value += amount_per_share * quantity

    def load_wallet(self):
        with open("wallet.log", "r+") as wallet_log:
            for line in wallet_log:
                line_arr = line.rstrip().split()
                self.register_transaction(line_arr[0], line_arr[1], float(line_arr[2]), float(line_arr[3]))
