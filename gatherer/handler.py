
import sys
import logging
import hashlib

from utils import load_django_models


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)
models = load_django_models()


def get_gatherer(source_slug):
    """Dynamically import the scraper modules."""
    module = __import__(
        'gatherers.{}'.format(
            source_slug.replace('-', '_')
        ), fromlist=[source_slug]
    )
    return module.Gatherer


def main(*args):

    sources = [s.slug for s in models.Source.objects.all() if s.slug]
    sources = [w for w in sources if w in args[0]] if args[0] else sources

    for source in sources:

        logger.info("Looking into {}...".format(source))

        gatherer = get_gatherer(source)()
        articles = gatherer.harvest()

        logger.info(
            "{} articles have been harvested".format(
                len(articles)
            )
        )

        logger.debug("Writing on database") if articles else logger.info(
            "No new articles to write on database"
        )

        nb_articles = len(models.Article.objects.filter(source=source))

        for article in articles:

            uid = "{}{}".format(
                article["source"],
                article["title"],
                str(article["published"])
            ).encode('utf-8')

            curr = models.Article(
                uid=hashlib.md5(uid).hexdigest(),
                source=article["source"],
                published=article["published"],
                extracted=article["extracted"],
                title=article["title"],
                text=article["text"],
                link=article["link"]
            )

            curr.save()

        logger.info(
            "{} new articles added to the database".format(
                len(models.Article.objects.filter(source=source)) - nb_articles
            )
        )


if __name__ == '__main__':
    main(sys.argv[1:])
