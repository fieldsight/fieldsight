# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0104_auto_20191120_1521'),
        ('fsforms', '0086_schedule_month_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportSyncSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('spreadsheet_id', models.CharField(max_length=250, null=True, blank=True)),
                ('grid_id', models.IntegerField(null=True, blank=True)),
                ('range', models.CharField(max_length=250, null=True, blank=True)),
                ('report_type', models.CharField(default='site_info', max_length=50, choices=[('site_info', 'Site Info'), ('site_progress', 'Site Progress'), ('form', 'Form')])),
                ('description', models.TextField()),
                ('last_synced_date', models.DateTimeField(null=True, blank=True)),
                ('form', models.ForeignKey(related_name='report_sync_settings', to='fsforms.FieldSightXF')),
                ('project', models.ForeignKey(related_name='report_sync_settings', to='fieldsight.Project')),
            ],
        ),
    ]
