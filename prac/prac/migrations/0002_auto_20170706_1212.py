# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commuting',
            old_name='ns',
            new_name='method_ns',
        ),
        migrations.AddField(
            model_name='commuting',
            name='time_ns',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commuting',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='education',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='families',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='housing',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='industries',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='occupation',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='pobnat',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='princstat',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='privhh',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='sexagemarriage',
            name='widowed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sexagemarriage',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AddField(
            model_name='socclass',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
        migrations.AlterField(
            model_name='csoref',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
    ]
