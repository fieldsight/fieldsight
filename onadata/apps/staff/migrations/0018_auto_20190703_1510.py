# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0017_auto_20190607_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='IdPassProof',
        ),
        migrations.AddField(
            model_name='attendance',
            name='IdPassProof',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]
