from rest_framework import serializers

from .models import Article, Source


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Article


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Source
