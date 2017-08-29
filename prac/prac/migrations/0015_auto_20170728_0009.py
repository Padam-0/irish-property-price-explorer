# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0014_auto_20170727_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sexagemarriage',
            name='uid',
            field=models.CharField(max_length=11),
        ),
    ]
