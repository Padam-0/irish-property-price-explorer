# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0002_auto_20170706_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='princstat',
            old_name='lffj',
            new_name='lookffirstjob',
        ),
    ]
