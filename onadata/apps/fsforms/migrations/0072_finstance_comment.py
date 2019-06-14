# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0071_editedsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='finstance',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
