# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import onadata.apps.fsforms.models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0072_objectpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', onadata.apps.fsforms.models.KpiUidField(uid_prefix='a')),
            ],
            options={
                'db_table': 'kpi_asset',
                'managed': False,
            },
        ),
    ]
