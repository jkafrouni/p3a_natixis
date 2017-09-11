from django.db import models


class Article(models.Model):
    uid = models.CharField(primary_key=True, editable=False, max_length=32)
    source = models.CharField(max_length=1024)
    published = models.DateTimeField(null=True)
    extracted = models.DateTimeField(null=True)
    title = models.CharField(max_length=1024)
    text = models.TextField(max_length=8096)
    link = models.URLField(blank=True, null=True)


class Source(models.Model):
    slug = models.SlugField(primary_key=True, max_length=128)
    link = models.URLField()
