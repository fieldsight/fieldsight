# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0081_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='site_featured_images',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
