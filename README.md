# p3a_natixis
Projet 3A - Ecole polytechnique x Natixis

## Setup

Install _pip_ and _virtualenv_. Create a virtual environment for the project (be sure to use Python 3.5.1) and launch
```
pip install -r requirements.txt
```

### Django setup

First, you have to setup a local postgreSQL database, here it all depends on your OS, so check it out on the internet. Name it (the database) `p3a` to match the settings on `server/api/settings.py`. 

Then you move to `server/` and just run 
```
./manage.py runserver
``` 

You'll then find your server at `http://127.0.0.1:8000/`

## Gathering the news

It is done by the files in the `gatherer/` folder. Basically an abstract class with instanciation for each news source.

It writes on db with thanks to django.

To launch it use 

```
python handler.py [sources]
```

where `[sources]` is an option, if you don't specify a source, it will launch the harvest for all the sources registered on the db. If you do it will launch the harvest for the sources you specified.

#### Examples
```
# 1.
python handler.py
# 2. 
python handler.py bbc
# 3.
python handler.py bbc reuters
```

The sources are found on the database, there's a table dedicated to them, when you submit a new *gatherer* you should do the following:

```
# Launch a django shell
$ cd server
$ ./manage.py shell
>>> from api.articles.models import Source
>>> s = Source(slug="cnn", link="http://rss.cnn.com/rss/edition_world.rss")
>>> s.save()
# ctrl + D to exit
# Save the data
$ ./manage.py dumpdata articles.source >! api/articles/fixtures/sources.json
# Then commit the changes on this fixture and your "gatherer", push your branch and submit a PR
```

This is made so that when you first setup the server you have this data ready for the handler; you just need to do the following:

```
$ cd server
$ ./manage.py loaddata sources
# And, for instance, to save the articles gathered (just as an example)
$ ./manage.py loaddata articles
```
