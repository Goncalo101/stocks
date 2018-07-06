from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from functools import reduce
from lxml import html
import operator
import requests


class Crawler:
    def __init__(self):
        self.running = True

        self.info = {"CAC40": {}, "DAX30": {}}
        # self.cac40_info = {}
        # self.dax30_info = {}

        self.time_of_request = datetime.now()

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(func=self.get_stock_listing,
                               trigger=IntervalTrigger(seconds=30),
                               id='Connection job',
                               name='Refresh information')

    # get_stock_listing should connect to boursorama, read the constituents of each index and modify the list of the
    # corresponding index with new values
    def get_stock_listing(self):
        self.time_of_request = datetime.now()

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
            self.info["CAC40"][info[0][k]] = {"LatestPrice": info[1][k], "Variation": info[2][k],
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
            self.info["DAX30"][info[0][k]] = {"LatestPrice": float(info[1][k]), "Variation": info[2][k],
                                              "OpeningPrice": float(info[3][k]), "HighestPrice": float(info[4][k]),
                                              "LowestPrice": float(info[5][k])}

        self.running = False

