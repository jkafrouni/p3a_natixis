
import time
import logging

import dateparser as dp
import pytz

import gatherer


URL_MAIN = [
    "http://feeds.bbci.co.uk/news/business/rss.xml",
    "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://feeds.bbci.co.uk/news/world/rss.xml"
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
        return "bbc"

    def get_pub_date(self, article_soup):
        tz = pytz.timezone("Europe/London")
        dt = dp.parse(
            article_soup.find("pubDate").text
        ).replace(tzinfo=tz)
        return dt

    def get_title(self, article_soup):
        return article_soup.find("title").text

    def get_text(self, article_soup):
        return article_soup.find("description").text

    def get_link(self, article_soup):
        return article_soup.find("link").text
