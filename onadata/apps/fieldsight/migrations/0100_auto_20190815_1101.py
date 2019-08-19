# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0099_site_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='weight',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
