# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0007_ageext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='ns',
            new_name='ed_ns',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='total',
            new_name='ed_total',
        ),
        migrations.RenameField(
            model_name='families',
            old_name='total',
            new_name='fam_total',
        ),
        migrations.RenameField(
            model_name='housing',
            old_name='age_ns',
            new_name='h_age_ns',
        ),
        migrations.RenameField(
            model_name='housing',
            old_name='age_total_hh',
            new_name='h_age_total_hh',
        ),
        migrations.RenameField(
            model_name='housing',
            old_name='oc_ns',
            new_name='occu_ns',
        ),
        migrations.RenameField(
            model_name='housing',
            old_name='oc_total_hh',
            new_name='occu_total_hh',
        ),
        migrations.RenameField(
            model_name='industries',
            old_name='other',
            new_name='ind_other',
        ),
        migrations.RenameField(
            model_name='industries',
            old_name='total',
            new_name='ind_total',
        ),
        migrations.RenameField(
            model_name='occupation',
            old_name='ns',
            new_name='occ_ns',
        ),
        migrations.RenameField(
            model_name='occupation',
            old_name='total',
            new_name='occ_total',
        ),
        migrations.RenameField(
            model_name='princstat',
            old_name='other',
            new_name='stat_other',
        ),
        migrations.RenameField(
            model_name='princstat',
            old_name='total',
            new_name='stat_total',
        ),
        migrations.RenameField(
            model_name='privhh',
            old_name='total',
            new_name='hstat_total',
        ),
        migrations.RenameField(
            model_name='privhh',
            old_name='total_hh',
            new_name='phh_total_hh',
        ),
        migrations.RenameField(
            model_name='sexagemarriage',
            old_name='total',
            new_name='mar_total',
        ),
        migrations.RenameField(
            model_name='socclass',
            old_name='other',
            new_name='class_other',
        ),
        migrations.RenameField(
            model_name='socclass',
            old_name='total',
            new_name='class_total',
        ),
        migrations.AddField(
            model_name='ageext',
            name='zoom',
            field=models.CharField(choices=[('region', 'region'), ('country', 'country'), ('county', 'county'), ('edist', 'edist'), ('area', 'area')], default='country', max_length=7),
        ),
    ]
