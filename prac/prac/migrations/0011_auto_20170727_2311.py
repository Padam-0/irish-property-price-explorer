# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0010_auto_20170727_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='housing',
            name='temp_abs',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housing',
            name='unoc_hol',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
