
import time
import logging

import dateparser as dp
import pytz

import gatherer


URL_MAIN = [
    "http://www.ft.com/rss/world",
    "http://www.ft.com/rss/world/americas",
    "http://www.ft.com/rss/world/americas/business",
    "http://www.ft.com/rss/world/americas/finance",
    "http://www.ft.com/rss/world/asia-pacific",
    "http://www.ft.com/rss/world/europe",
    "http://www.ft.com/rss/global-economy",
    "http://www.ft.com/rss/africa",
    "http://www.ft.com/rss/world/mideast/economy",
    "http://www.ft.com/rss/world/mideast/finance",
    "http://www.ft.com/rss/world/uk",
    "http://www.ft.com/rss/world/uk/business",
    "http://www.ft.com/companies/uk",
    "http://www.ft.com/rss/world/uk/economy",
    "http://www.ft.com/rss/world/us",
    "http://www.ft.com/rss/world/us/economy",
    "http://www.ft.com/rss/companies",  
    "http://www.ft.com/rss/companies/aerospace-defence",
    "http://www.ft.com/rss/companies/airlines",
    "http://www.ft.com/rss/companies/automobiles",
    "http://www.ft.com/rss/companies/banks",
    "http://www.ft.com/rss/companies/basic-resources",
    "http://www.ft.com/rss/companies/chemicals",
    "http://www.ft.com/rss/companies/construction",
    "http://www.ft.com/rss/companies/energy",
    "http://www.ft.com/rss/companies/financial-services",
    "http://www.ft.com/rss/companies/financials",
    "http://www.ft.com/rss/companies/food-beverage",
    "http://www.ft.com/rss/companies/health",
    "http://www.ft.com/rss/companies/healthcare",
    "http://www.ft.com/rss/companies/industrials",
    "http://www.ft.com/rss/companies/industrial-goods",
    "http://www.ft.com/rss/companies/insurance",
    "http://www.ft.com/rss/companies/media",
    "http://www.ft.com/rss/companies/mining",
    "http://www.ft.com/rss/companies/oil-gas",
    "http://www.ft.com/rss/companies/personal-goods",
    "http://www.ft.com/rss/companies/pharmaceuticals",
    "http://www.ft.com/rss/companies/property",
    "http://www.ft.com/rss/companies/rail",
    "http://www.ft.com/rss/companies/retail",
    "http://www.ft.com/rss/companies/retail-consumer",
    "http://www.ft.com/rss/companies/shipping",
    "http://www.ft.com/rss/companies/support-services",
    "http://www.ft.com/rss/companies/technology",
    "http://www.ft.com/rss/companies/telecoms",
    "http://www.ft.com/rss/companies/transport",
    "http://www.ft.com/rss/companies/travel-leisure",
    "http://www.ft.com/rss/companies/utilities"
]

logger = logging.getLogger(__name__)


class Gatherer(gatherer.AbstractGatherer):

    def __init__(self):
        self.soups = []
        for url in URL_MAIN:
            sp = gatherer.load_soup(url)
            self.soups.append(sp) if sp else logger.warning("Invalid soup")
            time.sleep(0.5)

    def get_articles(self):
        articles = []
        for soup in self.soups:
            articles.extend(
                soup.findAll("item")
            )
        return articles

    def get_source(self, article_soup):
        return "ft"

    def get_pub_date(self, article_soup):
        try:
            tz = pytz.timezone("US/Eastern")
            dt = dp.parse(
                article_soup.find("pubDate").text
            ).replace(tzinfo=tz)
        except AttributeError:
            logger.debug("No pub date informed")
            return None
        return dt

    def get_title(self, article_soup):
        return article_soup.find("title").text

    def get_text(self, article_soup):
        try:
            res = article_soup.find("description").text
            return res
        except AttributeError:
            return None

    def get_link(self, article_soup):
        return article_soup.find("link").text
