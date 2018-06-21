# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

# from bin.wallet import Wallet
from datetime import datetime, date
from functools import reduce
from lxml import html
# from third_party.highlight import highlight
import operator
import os
import requests

cac40_table = {}
dax30_table = {}

with open(os.path.join("data", "cac40.txt")) as cac40File:
    for line in cac40File:
        lineVec = line.split(' ', 1)
        cac40_table[lineVec[0]] = lineVec[1].rstrip()

with open(os.path.join("data", "dax30.txt")) as dax30File:
    for line in dax30File:
        lineVec = line.split(' ', 1)
        dax30_table[lineVec[0]] = lineVec[1].rstrip()

cac40_info = {}
dax30_info = {}

time_of_request = datetime.now()
start = True
version = "0.01"


# get_stock_listing should connect to boursorama, read the constituents of each index and modify the list of the
# corresponding index with new values
def get_stock_listing():
    stocks = []
    latest_price = []
    variation = []
    opening_price = []
    highest_price = []
    lowest_price = []

    info = [stocks, latest_price, variation, opening_price, highest_price, lowest_price]

    for i in range(1, 3):
        page = requests.get("https://www.boursorama.com/bourse/actions/cotations/page-" + str(
            i) + "?quotation_az_filter[market]=1rPCAC")
        tree = html.fromstring(page.content)

        stocks.append(tree.xpath('//li[@class="o-list-inline__item o-list-inline__item--middle"]/a/text()'))
        latest_price.append(tree.xpath(
            '//tr[@class="c-table__row"]/td[@class="c-table__cell c-table__cell--dotted u-text-right u-text-medium "]/span[@class="c-instrument c-instrument--last"]/text()'))
        variation.append(tree.xpath('//span[@class="c-instrument c-instrument--instant-variation"]/text()'))
        opening_price.append(tree.xpath('//span[@class="c-instrument c-instrument--open"]/text()'))
        highest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--high"]/text()'))
        lowest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--low"]/text()'))

    # Boursorama now displays the list of stocks in 2 pages which causes the loop above to generate a list with
    # two sublists, one for each page. It is much better to work with a single list, which is the purpose of
    # the following loop.
    for j in range(len(info)):
        info[j] = reduce(operator.concat, info[j])

    for k in range(40):
        cac40_info[info[0][k]] = {"LatestPrice": info[1][k], "Variation": info[2][k],
                                  "OpeningPrice": info[3][k], "HighestPrice": info[4][k],
                                  "LowestPrice": info[5][k]}

    # A lack of predictability in URLs brings the need to add another loop.
    # Resetting lists
    stocks = []
    latest_price = []
    variation = []
    opening_price = []
    highest_price = []
    lowest_price = []

    info = [stocks, latest_price, variation, opening_price, highest_price, lowest_price]

    for i in range(1, 3):
        page = requests.get("https://www.boursorama.com/bourse/actions/cotations/international/page-" + str(
            i) + "?international_quotation_az_filter%5Bcountry%5D=49&international_quotation_az_filter%5Bmarket%5D=5pDAX&international_quotation_az_filter%5Bletter%5D=&international_quotation_az_filter%5Bfilter%5D=")
        tree = html.fromstring(page.content)

        stocks.append(tree.xpath('//li[@class="o-list-inline__item o-list-inline__item--middle"]/a/text()'))
        latest_price.append(tree.xpath(
            '//tr[@class="c-table__row"]/td[@class="c-table__cell c-table__cell--dotted u-text-right u-text-medium "]/span[@class="c-instrument c-instrument--last"]/text()'))
        variation.append(tree.xpath('//span[@class="c-instrument c-instrument--instant-variation"]/text()'))
        opening_price.append(tree.xpath('//span[@class="c-instrument c-instrument--open"]/text()'))
        highest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--high"]/text()'))
        lowest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--low"]/text()'))

    for j in range(len(info)):
        info[j] = reduce(operator.concat, info[j])

    for k in range(29):
        dax30_info[info[0][k]] = {"LatestPrice": info[1][k], "Variation": info[2][k],
                                  "OpeningPrice": info[3][k], "HighestPrice": info[4][k],
                                  "LowestPrice": info[5][k]}


def display_stock_info(stock_list, stock):
    print('{0: <28} {1: <8} {2} {3: >8}'.format(stock, stock_list["LatestPrice"], stock_list["Variation"],
                                                stock_list["OpeningPrice"]))


# Program main loop
print("StockParser version %s" % version, sep="\n")
print("Initializing...")
get_stock_listing()

while start:
    print("Select an option:")
    print("0: Debug")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Refresh Stock Lists.")
    print("3: Show Info of a Given Stock.")
    print("4: Exit")

    option = input("> ")

    if option == "0":
        stock = input("Insert a stock > ").upper()
        stock = cac40_table[stock]

        display_stock_info(cac40_info[stock], stock)

        start = False

    if option == "1":
        index = input("Insert an index > ").upper()

        if index == "CAC40":
            keys = list(cac40_info.keys())
            for i in range(len(cac40_info)):  # Looking for a stock this way
                display_stock_info(cac40_info[keys[i]], keys[i])

            print("Data retrieved on: %s" % time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        elif index == "DAX30":
            keys = list(dax30_info.keys())
            for i in range(len(dax30_info)):
                display_stock_info(dax30_info[keys[i]], keys[i])

            print("Data retrieved on: %s" % time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        print("\n")

    elif option == "2":
        print("Refreshing...")
        time_of_request = datetime.now()
        get_stock_listing()
        print("Done\n")

    elif option == "3":
        index = input("Insert an index > ").upper()
        stock = input("Insert a stock > ").upper()

        if index == "CAC40":

            try:
                stock = cac40_table[stock]

                display_stock_info(cac40_info[stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        elif index == "DAX30":
            try:
                display_stock_info(dax30_info[stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        print("\n")

    elif option == "4":
        # Exit loop
        start = False

exit(0)
