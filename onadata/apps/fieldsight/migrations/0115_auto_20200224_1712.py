# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0114_projectmapfiltersmetrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmapfiltersmetrics',
            name='form_data_filters',
            field=jsonfield.fields.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='projectmapfiltersmetrics',
            name='site_information_filters',
            field=jsonfield.fields.JSONField(default=list),
        ),
    ]
