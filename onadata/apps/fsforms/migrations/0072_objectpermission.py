# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import onadata.apps.fsforms.models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0071_editedsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deny', models.BooleanField(default=False, help_text='Blocks inheritance of this permission when set to True')),
                ('inherited', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('uid', onadata.apps.fsforms.models.KpiUidField(uid_prefix='p')),
            ],
            options={
                'db_table': 'kpi_objectpermission',
                'managed': False,
            },
        ),
    ]
