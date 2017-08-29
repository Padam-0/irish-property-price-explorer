# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0013_auto_20170727_2312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housing',
            old_name='temp_abs',
            new_name='temp_unoc',
        ),
    ]
