# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0079_auto_20190522_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='site_basic_info',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='project',
            name='site_featured_images',
            field=jsonfield.fields.JSONField(default=list),
        ),
    ]
