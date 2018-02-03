# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management
# purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from datetime import datetime
from lxml import html
from third_party import highlight
import requests

proper_stock_list = []
version = "0.01"
start = True


def get_stock_listing(index):
    if index == "CAC40":
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
            proper_stock_list.append((stocks[i], latest_price[i], variation[i], opening_price[i],
                                      highest_price[i], lowest_price[i]))

        return proper_stock_list

    elif index == "DAX30":
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
            proper_stock_list.append([stocks[i], latest_price[i], variation[i], opening_price[i],
                                      highest_price[i], lowest_price[i]])

        return proper_stock_list


def display_stock_info(stock, index):
    for i in range(len(proper_stock_list)):
        if proper_stock_list[i][0] == stock.upper():
            print("Information for stock: %s" % proper_stock_list[i][0])

            print("Latest Price: %s" % proper_stock_list[i][1])

            print("Variation: %s" % highlight.highlight(proper_stock_list[i][2]))

            print("Opening Price: %s" % proper_stock_list[i][3])

            print("Highest Price in Session: %s" % proper_stock_list[i][4])

            print("Lowest Price in Session: %s" % proper_stock_list[i][5])

            print("\n")

            print("Data retrieved on: %s" % datetime.now())

            print("Data might be delayed by up to 15 minutes.")

            return

    print("Stock: %s is not in %s" % (stock, index))


while start:
    print("StockParser version %s" % version,  "Select an option to start:", sep="\n")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Refresh Stock Lists.")
    print("3: Show Info of a Given Stock.")
    print("4: Exit")

    option = input("> ")

    if option == "1":

        index = input("Insert an index > ").upper()
        get_stock_listing(index)

        for i in range(len(proper_stock_list)):

            print("Information for stock: %s" % proper_stock_list[i][0])

            print("Latest Price: %s" % proper_stock_list[i][1])

            print("Variation: %s" % highlight.highlight(proper_stock_list[i][2]))

            print("Opening Price: %s" % proper_stock_list[i][3])

            print("Highest Price in Session: %s" % proper_stock_list[i][4])

            print("Lowest Price in Session: %s" % proper_stock_list[i][5])

            print("\n")

    elif option == "2":

        get_stock_listing(index)

    elif option == "4":

        start = False

exit(0)

get_stock_listing("CAC40")
print(proper_stock_list)
display_stock_info("LVMH MOET VUITTON", "CAC40")

