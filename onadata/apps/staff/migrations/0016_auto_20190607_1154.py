# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0015_auto_20181101_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='IdPassProof',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='idPassDID',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
