
import django_filters
from rest_framework import viewsets, filters

from .serializers import ArticleSerializer, SourceSerializer
from .models import Article, Source


class ArticleTitleFilter(object):

    def filter_queryset(self, request, queryset, viewset):

        looking_for = request.query_params.get('in_title', None)

        if not looking_for:
            return queryset.all()

        return queryset.filter(title__search=looking_for)


class ArticleTextFilter(object):

    def filter_queryset(self, request, queryset, viewset):

        looking_for = request.query_params.get('in_text', None)

        if not looking_for:
            return queryset.all()

        return queryset.filter(text__search=looking_for)


class ArticleFilter(filters.FilterSet):

    published_gte = django_filters.DateTimeFilter(
        name='published', lookup_type='gte'
    )
    extracted_gte = django_filters.DateTimeFilter(
        name='extracted', lookup_type='gte'
    )

    published_lte = django_filters.DateTimeFilter(
        name='published', lookup_type='lte'
    )
    extracted_lte = django_filters.DateTimeFilter(
        name='extracted', lookup_type='lte'
    )

    class Meta:
        model = Article
        fields = ['extracted', 'published', 'source']


class ArticleViewSet(viewsets.ModelViewSet):
    """
    If you want to filter, you can do so by source, by published or
     extracted date with the following handles:

    * `source`
    * `published_gte` - this is with articles with dates greater than
     or equal to your date
    * `extracted_gte` - idem
    * `published_lte` - this is with articles with dates lesser than
     or equal to your date
    * `extracted_lte` - idem
    * `in_title` - enter a term to search for in the articles' titles
    * `in_text` - enter a term to search for in the articles' titles

    As an example if we want to get all cnn articles published after
     the 9th of October:

    ```/articles?published_gte=2016-10-09&source=cnn```

    """
    queryset = Article.objects.all()
    filter_class = ArticleFilter
    filter_backends = [
        filters.DjangoFilterBackend,
        ArticleTitleFilter,
        ArticleTextFilter
    ]
    serializer_class = ArticleSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
