# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from datetime import datetime
from lxml import html
from third_party import highlight
import requests

cac40_info = {'stocks': {}}
cac40_table = {"AC": "ACCOR", "AI": "AIR LIQUIDE" ,"AIR": "AIRBUS", "AMT": " ARCELORMITTAL", "ATO": "ATOS", "CS": "AXA",
               "BNP": "BNP PARIBAS BR-A", "EN": "BOUYGUES", "CAP": "CAPGEMINI",  "CA": "CARREFOUR",
               "ACA": "CREDIT AGRICOLE SA", "ENGI": "ENGIE", "BN": "DANONE","EI": "ESSILOR INTL", "KER": "KERING (Ex: PPR)",
               "OR": "L'OREAL", "LHN": "LAFARGEHOLCIM N", "LR": "LEGRAND", "MC":  "LVMH MOET VUITTON",
               "ML": "MICHELIN N", "ORA": "ORANGE (ex: FRANCE TELECOM)", "PRI": "PERNOD RICARD", "UG": "PEUGEOT",
               "PUB": "PUBLICIS GRP", "RNO": "RENAULT", "SAF": "SAFRAN", "SGO": "SAINT-GOBAIN", "SAN": "SANOFI",
               "SU": "SCHNEIDER E.SE", "GLE": "SOCIETE GENERALE", "SW": "SODEXO", "OLB": "SOLVAY", "STM": "STMICROELECTR",
               "FTI": "TECHNIP", "FP": "TOTAL", "UL": "UNIBAIL-RODAMCO", "FR": "VALEO", "VIE": "VEOLIA ENVIRONMENT",
               "DG": "VINCI", "VIV": "VIVENDI"}

dax30_info = {'stocks': {}}
time_of_request = datetime.now()
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
            cac40_info["stocks"][stocks[i]] = {"LatestPrice": latest_price[i], "Variation": variation[i],
                                               "OpeningPrice": opening_price[i], "HighestPrice": highest_price[i],
                                               "LowestPrice": lowest_price[i]}

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
            dax30_info["stocks"][stocks[i]] = {"LatestPrice": latest_price[i], "Variation": variation[i],
                                               "OpeningPrice": opening_price[i], "HighestPrice": highest_price[i],
                                               "LowestPrice": lowest_price[i]}


def display_stock_info(stock_list, stock):
    print("\n")

    print("Information for stock: %s" % stock)
    print("Latest Price: %s" % stock_list["LatestPrice"])
    print("Variation: %s" % highlight.highlight(stock_list["Variation"]))
    print("Opening Price: %s" % stock_list["OpeningPrice"])
    print("Highest Price in Session: %s" % stock_list["HighestPrice"])
    print("Lowest Price in Session: %s" % stock_list["LowestPrice"])

    print("\n")

    print("Data retrieved on: %s" % time_of_request)
    print("Data might be delayed by up to 15 minutes.")


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

        display_stock_info(cac40_info["stocks"][stock], stock)

        start = False

    if option == "1":
        index = input("Insert an index > ").upper()

        if index == "CAC40":
            keys = list(cac40_info["stocks"].keys())
            for i in range(len(cac40_info["stocks"])):  # Looking for a stock this way
                display_stock_info(cac40_info["stocks"][keys[i]], keys[i])

        elif index == "DAX30":
            keys = list(dax30_info["stocks"].keys())
            for i in range(len(dax30_info["stocks"])):
                display_stock_info(dax30_info["stocks"][keys[i]], keys[i])

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

                display_stock_info(cac40_info["stocks"][stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        elif index == "DAX30":
            try:
                display_stock_info(dax30_info["stocks"][stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        print("\n")

    elif option == "4":
        # Exit loop
        start = False

exit(0)
