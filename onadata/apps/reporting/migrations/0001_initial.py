# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Site'), (1, b'Region'), (2, b'Project'), (3, b'Team'), (4, b'User'), (5, b'Time Series')])),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=250)),
                ('attributes', jsonfield.fields.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(related_name='report_settings', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('shared_with', models.ManyToManyField(related_name='shared_report_settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
