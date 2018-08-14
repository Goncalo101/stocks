from datetime import datetime
from bin.crawler import Crawler
import atexit
import os
import time


class Wallet(Crawler):
    def __init__(self):
        super().__init__()

        self.funds = 0.0
        self.market_value = 0.0
        self.transaction_history = []
        self.wallet = {}

        self.conversion_table = {"CAC40": {}, "DAX30": {}}

        # Load conversion table from file
        with open(os.path.join("data", "cac40.txt")) as cac40File:
            for line in cac40File:
                line_vec = line.split(' ', 1)
                self.conversion_table["CAC40"][line_vec[0]] = line_vec[1].rstrip()

        with open(os.path.join("data", "dax30.txt")) as dax30File:
            for line in dax30File:
                line_vec = line.split(' ', 1)
                self.conversion_table["DAX30"][line_vec[0]] = line_vec[1].rstrip()

    def check_crawler(self):
        print("Loading data, please wait...")

        while self.running:
            time.sleep(10)

    def terminate(self):
        atexit.register(lambda: self.scheduler.shutdown())

    def add_funds(self, amount):
        self.funds += amount

    def remove_funds(self, amount):
        self.add_funds(-amount)

    def recalculate_market_value(self):
        # self.market_value = 0
        # self.update_market_value(index, stock_name)
        pass

    def update_market_value(self, index, stock_name):
        full_name = self.translate(stock_name, index)
        self.market_value += self.wallet[stock_name]["Quantity"] * self.info[index][full_name]["LatestPrice"]

    def register_transaction(self, transaction_type, index, stock, quantity, price):  # Negative quantity means sale
        self.check_crawler()

        transaction_value = quantity * price
        transaction_time = str(datetime.now())

        self.transaction_history.append([transaction_type, stock, abs(quantity), price, abs(transaction_value), transaction_time])

        try:  # Try to update values in dictionary
            self.wallet[stock]["Quantity"] += quantity
            self.wallet[stock]["Cost"] += transaction_value
            self.wallet[stock]["Price"] = self.wallet[stock]["Cost"] / self.wallet[stock]["Quantity"]

        except KeyError:
            self.wallet[stock] = {"Quantity": quantity, "Price": price, "Cost": transaction_value, "Index": index}

        self.update_market_value(index, stock)

        with open("wallet.out", "a") as wallet_log:
            wallet_log.write('{0} {1} {2} {3}\n'.format(stock, quantity, price, transaction_value))

    def register_dividend(self, amount_per_share, stock):
        quantity = self.wallet[stock]["Quantity"]

        self.funds += amount_per_share * quantity

    def load_wallet(self, wallet_file):
        with open(wallet_file, "r+") as wallet_log:
            for line in wallet_log:
                line_arr = line.rstrip().split()
                self.register_transaction(line_arr[0], line_arr[1], line_arr[2], float(line_arr[3]), float(line_arr[4]))

    def get_info(self):
        return self.info

    def get_time(self):
        return self.time_of_request

    def translate(self, stock, index):
        return self.conversion_table[index][stock]

    def get_market_value(self):
        return '{0:,.2f}'.format(self.market_value)
