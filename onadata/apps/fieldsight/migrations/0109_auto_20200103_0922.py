# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0108_remove_superorganization_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemetaattranshistory',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(1, 'By submission'), (2, 'By change in meta attributes'), (3, 'Meta Generation')]),
        ),
    ]
