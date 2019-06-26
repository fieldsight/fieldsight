# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fieldsight', '0083_progresssettings_sitemetaattrhistory_siteprogresshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='progresssettings',
            name='user',
            field=models.ForeignKey(related_name='progress_settings', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
