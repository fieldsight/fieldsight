# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0089_auto_20191209_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsyncsettings',
            name='form',
            field=models.ForeignKey(related_name='report_sync_settings', blank=True, to='fsforms.FieldSightXF', null=True),
        ),
    ]
