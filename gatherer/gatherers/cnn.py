
import time
import logging

import dateparser as dp
import pytz

import gatherer


URL_MAIN = [
    "http://rss.cnn.com/rss/edition.rss",
    "http://rss.cnn.com/rss/edition_world.rss",
    "http://rss.cnn.com/rss/edition_europe.rss",
    "http://rss.cnn.com/rss/edition_africa.rss",
    "http://rss.cnn.com/rss/edition_americas.rss",
    "http://rss.cnn.com/rss/edition_asia.rss",
    "http://rss.cnn.com/rss/edition_meast.rss",
    "http://rss.cnn.com/rss/edition_us.rss",
    "http://rss.cnn.com/rss/money_news_international.rss",
    "http://rss.cnn.com/rss/edition_technology.rss",
    "http://rss.cnn.com/rss/edition_space.rss",
    "http://rss.cnn.com/rss/edition_entertainment.rss",
    "http://rss.cnn.com/rss/cnn_latest.rss"
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
        return "cnn"

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
