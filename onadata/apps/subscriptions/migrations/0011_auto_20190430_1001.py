# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_auto_20190415_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='initiated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='updated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
