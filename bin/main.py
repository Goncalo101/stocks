# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management
# purposes.
# This is a web scraper, no api is being used, so it is quite limited.

from lxml import html
import requests

properStockList = []

def getStockListing(index):
    if index == "CAC40":
        page = requests.get("http://www.boursorama.com/bourse/actions/cours_az.phtml?MARCHE=1rPCAC")
        tree = html.fromstring(page.content)

        stocks = tree.xpath('//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-libelle"]/a/text()')
        latestPrice = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-last"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-last"]/span/text()')
        variation = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var"]/span/text()')
        openingPrice = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-open"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-open"]/span/text()')
        highestPrice = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-high"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-high"]/span/text()')
        lowestPrice = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-low"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-low"]/span/text()')
        variationFrom1Jan = tree.xpath(
            '//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/span/text()|//table[@class="block alt list sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/text()')

        for i in range(40):
            properStockList.append((stocks[i], latestPrice[i], variation[i], openingPrice[i],
                                    highestPrice[i], lowestPrice[i]))

        return properStockList