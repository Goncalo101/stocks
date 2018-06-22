# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from bin.crawler import Crawler
from bin.wallet import Wallet
from third_party.highlight import highlight
import atexit
import os
import time

cac40_table = {}
dax30_table = {}

# Load conversion table from file
with open(os.path.join("data", "cac40.txt")) as cac40File:
    for line in cac40File:
        lineVec = line.split(' ', 1)
        cac40_table[lineVec[0]] = lineVec[1].rstrip()

with open(os.path.join("data", "dax30.txt")) as dax30File:
    for line in dax30File:
        lineVec = line.split(' ', 1)
        dax30_table[lineVec[0]] = lineVec[1].rstrip()

start = True
version = "0.02"


def display_stock_info(stock_list, stock):
    print('{0: <28} {1: >8} {2} {3: >8}'.format(stock, stock_list["LatestPrice"], highlight(stock_list["Variation"]),
                                                stock_list["OpeningPrice"]))


def get_stock_info(stock_list, stock):  # Returns a dictionary containing stock information
    return stock_list[stock]


# Program main loop
print("stocks version %s" % version, sep="\n")
crawler = Crawler()
wallet = Wallet()

print("Loading data, please wait...")


while crawler.running:
    time.sleep(5)

while start:
    print("\nSelect an option:")
    print("0: Debug")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Show Info of a Given Stock.")
    print("3: Exit")

    option = input("> ")

    if option == "0":

        wallet.load_wallet()
        print(wallet.wallet)

    if option == "1":
        index = input("Insert an index > ").upper()

        print('{0: <28} {1: >8} {2} {3: >8}'.format("Constituent", "Latest", "Variation", "Opening"))  # Table header

        if index == "CAC40":

            keys = sorted(list(crawler.cac40_info.keys()))
            for i in range(len(crawler.cac40_info)):
                display_stock_info(crawler.cac40_info[keys[i]], keys[i])

            print("Data retrieved on: %s" % crawler.time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        elif index == "DAX30":

            keys = sorted(list(crawler.dax30_info.keys()))
            for i in range(len(crawler.dax30_info)):
                display_stock_info(crawler.dax30_info[keys[i]], keys[i])

            print("Data retrieved on: %s" % crawler.time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        print("\n")

    elif option == "2":
        index = input("Insert an index > ").upper()
        stock = input("Insert a stock > ").upper()

        if index == "CAC40":

            try:
                stock = cac40_table[stock]

                display_stock_info(crawler.cac40_info[stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        elif index == "DAX30":
            try:
                stock = dax30_table[stock]

                display_stock_info(crawler.dax30_info[stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        print("\n")

    elif option == "3":
        # Exit loop
        start = False

atexit.register(lambda: crawler.scheduler.shutdown())  # Properly terminate scheduler
exit(0)
