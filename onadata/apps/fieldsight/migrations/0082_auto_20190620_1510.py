# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0081_reportdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdata',
            name='app_os_version',
            field=models.CharField(max_length=31, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reportdata',
            name='app_version',
            field=models.CharField(max_length=31, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reportdata',
            name='device_name',
            field=models.CharField(max_length=31, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reportdata',
            name='fcm_reg_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
