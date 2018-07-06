# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from bin.wallet import Wallet
from third_party.highlight import highlight

start = True
version = "0.02"


def display_stock_info(stock_list, stock):
    print('{0: <28} {1: >8} {2} {3: >8}'.format(stock, stock_list["LatestPrice"], highlight(stock_list["Variation"]),
                                                stock_list["OpeningPrice"]))


def get_stock_info(stock_list, stock):  # Returns a dictionary containing stock information
    return stock_list[stock]


def show_index_info(index):
    info = wallet.get_info()[index]
    stocks_in_index = sorted(list(info.keys()))

    print('{0: <28} {1: >8} {2} {3: >8}'.format("Constituent", "Latest", "Variation", "Opening"))  # Table header

    i = 0
    while i < len(info):
        stock = stocks_in_index[i]
        display_stock_info(info[stock], stock)
        i += 1

    print("Data retrieved on: %s" % wallet.get_time())
    print("Data might be delayed by up to 15 minutes.\n")


# Program main loop
print("stocks version %s" % version, sep="\n")

wallet = Wallet()


def handle_option2():
    index = input("Insert an index > ").upper()
    stock = input("Insert a stock > ").upper()

    try:
        stock = wallet.translate(stock, index)

        wallet.check_crawler()

        # Table header
        print('{0: <28} {1: >8} {2} {3: >8}'.format("Constituent", "Latest", "Variation", "Opening"))
        display_stock_info(wallet.get_info()[index][stock], stock)

    except KeyError:
        print("The stock %s does not exist in %s\n" % (stock, index))

    else:
        print("\nData retrieved on: %s" % wallet.get_time())
        print("Data might be delayed by up to 15 minutes.\n")


while start:
    print("\nSelect an option:")
    print("0: Debug")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Show Info of a Given Stock.")
    print("3: Load wallet.")
    print("4: Exit")

    option = input("> ")

    if option == "1":
        index = input("Insert an index > ").upper()

        show_index_info(index)

    elif option == "2":
        handle_option2()

    elif option == "3":
        wallet_file = input("Insert wallet file name > ")

        wallet.load_wallet(wallet_file)

        print("Market value: %s\n" % wallet.get_market_value())

    elif option == "4":
        # Exit loop
        start = False

wallet.terminate()  # Properly terminate scheduler
exit(0)
