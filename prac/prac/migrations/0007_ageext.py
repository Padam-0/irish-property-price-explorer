# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0006_auto_20170706_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeExt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('uid', models.CharField(max_length=10)),
                ('age_04_m', models.IntegerField()),
                ('age_59_m', models.IntegerField()),
                ('age_1014_m', models.IntegerField()),
                ('age_1519_m', models.IntegerField()),
                ('age_2024_m', models.IntegerField()),
                ('age_2529_m', models.IntegerField()),
                ('age_3034_m', models.IntegerField()),
                ('age_3539_m', models.IntegerField()),
                ('age_4044_m', models.IntegerField()),
                ('age_4549_m', models.IntegerField()),
                ('age_5054_m', models.IntegerField()),
                ('age_5559_m', models.IntegerField()),
                ('age_6064_m', models.IntegerField()),
                ('age_6569_m', models.IntegerField()),
                ('age_7074_m', models.IntegerField()),
                ('age_7579_m', models.IntegerField()),
                ('age_8084_m', models.IntegerField()),
                ('age_85p_m', models.IntegerField()),
                ('age_04_f', models.IntegerField()),
                ('age_59_f', models.IntegerField()),
                ('age_1014_f', models.IntegerField()),
                ('age_1519_f', models.IntegerField()),
                ('age_2024_f', models.IntegerField()),
                ('age_2529_f', models.IntegerField()),
                ('age_3034_f', models.IntegerField()),
                ('age_3539_f', models.IntegerField()),
                ('age_4044_f', models.IntegerField()),
                ('age_4549_f', models.IntegerField()),
                ('age_5054_f', models.IntegerField()),
                ('age_5559_f', models.IntegerField()),
                ('age_6064_f', models.IntegerField()),
                ('age_6569_f', models.IntegerField()),
                ('age_7074_f', models.IntegerField()),
                ('age_7579_f', models.IntegerField()),
                ('age_8084_f', models.IntegerField()),
                ('age_85p_f', models.IntegerField()),
                ('age_0', models.IntegerField()),
                ('age_1', models.IntegerField()),
                ('age_2', models.IntegerField()),
                ('age_3', models.IntegerField()),
                ('age_4', models.IntegerField()),
                ('age_5', models.IntegerField()),
                ('age_6', models.IntegerField()),
                ('age_7', models.IntegerField()),
                ('age_8', models.IntegerField()),
                ('age_9', models.IntegerField()),
                ('age_10', models.IntegerField()),
                ('age_11', models.IntegerField()),
                ('age_12', models.IntegerField()),
                ('age_13', models.IntegerField()),
                ('age_14', models.IntegerField()),
                ('age_15', models.IntegerField()),
                ('age_16', models.IntegerField()),
                ('age_17', models.IntegerField()),
                ('age_18', models.IntegerField()),
                ('age_19', models.IntegerField()),
            ],
        ),
    ]
