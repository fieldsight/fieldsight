# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fsforms', '0090_auto_20191209_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsyncsettings',
            name='updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reportsyncsettings',
            name='user',
            field=models.ForeignKey(related_name='report_sync_settings', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
