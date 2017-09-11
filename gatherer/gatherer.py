
from urllib.request import urlopen
import urllib.error
import http.client
import logging

from bs4 import BeautifulSoup
from django.utils import timezone


logger = logging.getLogger(__name__)


def load_soup(url):
    """ Return a bs object """
    logger.debug('Loading url: {}'.format(url))
    try:
        html_page = urlopen(url).read()
    except (http.client.IncompleteRead, urllib.error.URLError):
        logger.warning("Could not read the page")
        return None
    logger.debug('Parsing with BS')
    return BeautifulSoup(html_page, 'lxml-xml')


class AbstractGatherer(object):

    def harvest(self):
        """ Return the list of articles, each on a formatted dict """
        results = []
        articles = self.get_articles()

        for article in articles:
            current = {
                "source": self.get_source(article),
                "published": self.get_pub_date(article),
                "extracted": timezone.now(),
                "title": self.get_title(article),
                "text": self.get_text(article),
                "link": self.get_link(article),
                "tags": self.get_tags(article)
            }

            if current["text"] and current["published"]:
                results.append(current)

        return results

    def get_articles(self):
        """ Return the list of available articles, each on its soup form """
        raise NotImplementedError

    def get_source(self, article_soup):
        """ Return the source of the article """
        raise NotImplementedError

    def get_pub_date(self, article_soup):
        """ Return publication date in a datetime object """
        raise NotImplementedError

    def get_title(self, article_soup):
        """ Return the title of the article """
        raise NotImplementedError

    def get_text(self, article_soup):
        """ Return the text of the article """
        raise NotImplementedError

    def get_link(self, article_soup):
        """ Return the tags of the article if they exist """
        return None

    def get_tags(self, article_soup):
        """ Return the tags of the article if they exist """
        return None
