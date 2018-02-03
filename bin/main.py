# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from datetime import datetime
from lxml import html
from third_party import highlight
import requests

cac40_info = {'stocks'}
dax30_info = []
time = datetime.now()
start = True
version = "0.01"

# get_stock_listing should connect to boursorama, read the constituents of each index and modify the list of the
# corresponding index with new values
def get_stock_listing():
        page = requests.get("http://www.boursorama.com/bourse/actions/cours_az.phtml?MARCHE=1rPCAC")
        tree = html.fromstring(page.content)

        stocks = tree.xpath('//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-libelle"]/a/text()')
        latest_price = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-last"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-last"]/span/text()')
        variation = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var"]/span/text()')
        opening_price = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-open"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-open"]/span/text()')
        highest_price = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-high"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-high"]/span/text()')
        lowest_price = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-low"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-low"]/span/text()')
        variation_from1_jan = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/text()')

        # Each stock is going to be inside a vector inside a list
        for i in range(40):
            cac40_info.append({stocks[i]})
            # cac40_info.append((stocks[i], latest_price[i], variation[i], opening_price[i],
            #                    highest_price[i], lowest_price[i]))

        page = requests.get("http://www.boursorama.com/bourse/actions/inter_az.phtml?PAYS=49&BI=5pDAX")
        tree = html.fromstring(page.content)

        stocks = tree.xpath('//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-libelle"]/a/text()')
        latest_price = tree.xpath(
            '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-last"]/span/text()')
        variation = tree.xpath('//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-var"]/span/text()')
        opening_price = tree.xpath(
            '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-open"]/span/text()')
        highest_price = tree.xpath(
            '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-high"]/span/text()')
        lowest_price = tree.xpath(
            '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-low"]/span/text()')
        variation_from1_jan = tree.xpath(
            '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/text()')

        for i in range(30):
            dax30_info.append([stocks[i], latest_price[i], variation[i], opening_price[i],
                               highest_price[i], lowest_price[i]])


def lookup_stock(stock, index):
    if index == "CAC40":
        for i in range(len(cac40_info)):
            if stock in cac40_info[i][0]:
                return cac40_info[i]

    elif index == "DAX30":
        for i in range(len(dax30_info)):
            if stock in dax30_info[i]:
                return dax30_info[i]


def display_stock_info(stock_list):
    if stock_list is None:
        print("Could not find stock in index.")

    else:
        print("\n")

        print("Information for stock: %s" % stock_list[0])
        print("Latest Price: %s" % stock_list[1])
        print("Variation: %s" % highlight.highlight(stock_list[2]))
        print("Opening Price: %s" % stock_list[3])
        print("Highest Price in Session: %s" % stock_list[4])
        print("Lowest Price in Session: %s" % stock_list[5])

        print("\n")

        print("Data retrieved on: %s" % time)
        print("Data might be delayed by up to 15 minutes.")


# Program main loop
print("StockParser version %s" % version, sep="\n")
print("Initializing...")
get_stock_listing()

while start:
    print("Select an option:")
    print("0: Debug")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Refresh Stock Lists.")  # The need to generate at least 2 arrays might be too resource intensive
    print("3: Show Info of a Given Stock.")
    print("4: Exit")

    option = input("> ")

    if option == "0":
        print(cac40_info)
        print(cac40_info["ACCOR"]["price"])

    if option == "1":
        index = input("Insert an index > ").upper()

        if index == "CAC40":
            for i in range(len(cac40_info)):  # Looking for a stock this way
                display_stock_info(cac40_info[i])

        elif index == "DAX30":
            for i in range(len(dax30_info)):
                display_stock_info(dax30_info[i])

        print("\n")

    elif option == "2":
        print("Refreshing...")
        time = datetime.now()
        get_stock_listing()
        print("Done\n")

    elif option == "3":
        index = input("Insert an index > ").upper()
        stock = input("Insert a stock > ").upper()

        display_stock_info(lookup_stock(stock, index))

        print("\n")

    elif option == "4":
        # Exit loop
        start = False

exit(0)
