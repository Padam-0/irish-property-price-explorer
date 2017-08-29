# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0011_auto_20170727_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='temp_abs',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='housing',
            name='unoc_hol',
            field=models.IntegerField(),
        ),
    ]
