# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0087_reportsyncsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsyncsettings',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
