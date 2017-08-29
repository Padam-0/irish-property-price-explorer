# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0004_families_adol'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privhh',
            old_name='ge_eigh_phh',
            new_name='ge_eight_phh',
        ),
    ]
