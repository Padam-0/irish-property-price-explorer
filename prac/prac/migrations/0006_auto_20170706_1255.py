# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0005_auto_20170706_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='princstat',
            old_name='lookffirstjob',
            new_name='lffj',
        ),
    ]
