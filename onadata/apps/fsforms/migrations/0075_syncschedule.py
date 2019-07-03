# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0074_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('schedule', models.CharField(default='M', max_length=2, choices=[('D', 'Daily'), ('W', 'Weekly'), ('F', 'Fortnightly'), ('M', 'Monthly')])),
                ('fxf', models.OneToOneField(related_name='sync_schedule', to='fsforms.FieldSightXF')),
            ],
        ),
    ]
