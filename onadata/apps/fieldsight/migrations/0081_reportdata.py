# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fieldsight', '0080_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, 'Mobile'), (1, 'web')])),
                ('device', models.CharField(max_length=31, null=True, blank=True)),
                ('fcm_reg_id', models.CharField(max_length=255)),
                ('app_version', models.CharField(max_length=31)),
                ('app_os_version', models.CharField(max_length=31)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True)),
                ('message_type', models.IntegerField(default=3, choices=[(0, 'Bug'), (1, 'Crash'), (2, 'Inaccurate Data'), (3, 'Others')])),
                ('message', models.TextField()),
                ('device_name', models.CharField(max_length=31)),
                ('user', models.ForeignKey(related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
