# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0104_auto_20191120_1521'),
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsettings',
            name='add_to_templates',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reportsettings',
            name='project',
            field=models.ForeignKey(related_name='report_settings', default=1, to='fieldsight.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportsettings',
            name='owner',
            field=models.ForeignKey(related_name='report_settings', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportsettings',
            name='shared_with',
            field=models.ManyToManyField(related_name='shared_report_settings', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
