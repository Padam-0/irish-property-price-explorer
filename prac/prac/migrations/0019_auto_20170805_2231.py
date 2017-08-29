# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0018_auto_20170805_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housing',
            old_name='b01_00',
            new_name='b01_10',
        ),
    ]
