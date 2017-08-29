# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0008_auto_20170725_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='ed',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='quality',
            field=models.CharField(default='good', max_length=4),
            preserve_default=False,
        ),
    ]
