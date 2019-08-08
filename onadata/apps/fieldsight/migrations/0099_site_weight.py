# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0098_auto_20190724_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
