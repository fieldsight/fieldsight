# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_auto_20190607_1154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='idPassDID',
            new_name='IdPassDID',
        ),
    ]
