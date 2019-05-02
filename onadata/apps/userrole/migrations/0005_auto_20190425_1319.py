# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0004_userrole_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='ended_at',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
    ]
