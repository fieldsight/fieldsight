# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0097_auto_20200122_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finstance',
            name='team_fxf',
        ),
    ]
