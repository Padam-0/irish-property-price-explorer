# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0019_auto_20170805_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='uid',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='housing',
            name='zoom',
            field=models.CharField(max_length=70, default='country', choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')]),
        ),
    ]
