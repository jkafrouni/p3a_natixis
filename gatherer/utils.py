
import os
import sys

import django


def load_django_models():
    base = os.path.dirname(__file__)
    django_fp = os.path.join(os.path.dirname(base), 'server')
    sys.path.insert(1, django_fp)
    os.environ.setdefault("PYTHONPATH", django_fp)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    django.setup()

    return __import__('api.articles.models', fromlist=['models'])
