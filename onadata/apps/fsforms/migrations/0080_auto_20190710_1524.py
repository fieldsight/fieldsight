# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fsforms', '0079_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editedsubmission',
            name='new',
        ),
        migrations.AddField(
            model_name='editedsubmission',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 10, 15, 24, 18, 392189), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editedsubmission',
            name='json',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='editedsubmission',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='editedsubmission',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
