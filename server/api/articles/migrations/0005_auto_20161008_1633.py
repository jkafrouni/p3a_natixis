# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20161008_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.URLField(blank=True, default=None),
            preserve_default=False,
        ),
    ]