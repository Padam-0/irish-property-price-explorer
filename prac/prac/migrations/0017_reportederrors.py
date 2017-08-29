# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0016_auto_20170728_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportedErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('marker_uid', models.IntegerField()),
                ('address_error', models.BooleanField()),
                ('location_error', models.BooleanField()),
                ('date_error', models.BooleanField()),
                ('price_error', models.BooleanField()),
                ('other_info', models.CharField(max_length=500)),
            ],
        ),
    ]
