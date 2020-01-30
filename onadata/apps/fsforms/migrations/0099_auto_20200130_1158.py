# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_reportsettings_filter'),
        ('fsforms', '0098_remove_finstance_team_fxf'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsyncsettings',
            name='report',
            field=models.ForeignKey(related_name='report_sync_settings', blank=True, to='reporting.ReportSettings', null=True),
        ),
        migrations.AlterField(
            model_name='reportsyncsettings',
            name='report_type',
            field=models.CharField(default='site_info', max_length=50, choices=[('site_info', 'Site Info'), ('site_progress', 'Site Progress'), ('form', 'Form'), ('custom', 'Custom')]),
        ),
    ]
