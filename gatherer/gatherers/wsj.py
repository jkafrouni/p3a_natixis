
import time
import logging

import dateparser as dp
import pytz

import gatherer


URL_MAIN = [
    "http://www.wsj.com/xml/rss/3_7085.xml",
    "http://www.wsj.com/xml/rss/3_7014.xml",
    "http://www.wsj.com/xml/rss/3_7031.xml",
    "http://www.wsj.com/xml/rss/3_7455.xml",
    "http://www.wsj.com/xml/rss/3_7041.xml",
    "http://www.wsj.com/xml/rss/3_7201.xml"
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
        return "wsj"

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
