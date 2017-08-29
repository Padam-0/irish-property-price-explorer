# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0017_reportederrors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housing',
            old_name='b01_05',
            new_name='b01_00',
        ),
        migrations.RenameField(
            model_name='housing',
            old_name='g06',
            new_name='g11',
        ),
    ]
