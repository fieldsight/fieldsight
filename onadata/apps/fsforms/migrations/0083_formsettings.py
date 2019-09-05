# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fsforms', '0082_stage_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('types', django.contrib.postgres.fields.ArrayField(default=[], base_field=models.IntegerField(), size=None)),
                ('regions', django.contrib.postgres.fields.ArrayField(default=[], base_field=models.IntegerField(), size=None)),
                ('notify_incomplete_schedule', models.BooleanField(default=False)),
                ('donor_visibility', models.BooleanField(default=False)),
                ('can_edit', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('form', models.OneToOneField(related_name='settings', to='fsforms.FieldSightXF')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
