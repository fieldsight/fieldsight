# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0085_progresssettings_deployed'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprogresshistory',
            name='setting',
            field=models.ForeignKey(related_name='progress', blank=True, to='fieldsight.ProgressSettings', null=True),
        ),
    ]
