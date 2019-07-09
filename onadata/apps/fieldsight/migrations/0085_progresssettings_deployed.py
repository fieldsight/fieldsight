# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0084_progresssettings_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='progresssettings',
            name='deployed',
            field=models.BooleanField(default=False),
        ),
    ]
