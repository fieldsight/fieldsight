# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0089_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progresssettings',
            name='pull_integer_form_question',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
