# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0009_auto_20170727_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='ageext',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commuting',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='education',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='families',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housing',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industries',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='occupation',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pobnat',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='princstat',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='privhh',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sexagemarriage',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socclass',
            name='year',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
    ]
