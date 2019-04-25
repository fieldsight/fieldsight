# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0072_organization_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='is_active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]
