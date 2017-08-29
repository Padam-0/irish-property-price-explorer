# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0015_auto_20170728_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sexagemarriage',
            name='uid',
            field=models.CharField(max_length=10),
        ),
    ]
