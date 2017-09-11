
import re
import time
import logging

import dateparser as dp
import pytz

import gatherer


URL_MAIN = [
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.reuters.com/Reuters/worldNews",
    "http://feeds.reuters.com/reuters/companyNews",
    "http://feeds.reuters.com/Reuters/PoliticsNews",
    "http://feeds.reuters.com/reuters/scienceNews",
    "http://feeds.reuters.com/reuters/technologyNews",
    "http://feeds.reuters.com/reuters/topNews",
    "http://feeds.reuters.com/news/wealth",
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
        return "reuters"

    def get_pub_date(self, article_soup):
        tz = pytz.timezone("US/Eastern")
        dt = dp.parse(
            article_soup.find("pubDate").text
        ).replace(tzinfo=tz)
        return dt

    def get_title(self, article_soup):
        return article_soup.find("title").text

    def get_text(self, article_soup):
        raw_text = article_soup.find("description").text
        return re.sub("<div[\S\s]*", "", raw_text)

    def get_link(self, article_soup):
        return article_soup.find("link").text
