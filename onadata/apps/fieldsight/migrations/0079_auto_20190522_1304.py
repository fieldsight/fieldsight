# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0078_merge'),
    ]

    operations = [
        migrations.AlterField('sitetype', 'identifier', models.CharField(max_length=255, verbose_name='ID'))
    ]
