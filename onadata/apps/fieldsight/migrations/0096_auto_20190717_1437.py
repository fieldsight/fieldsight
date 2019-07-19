# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0095_auto_20190711_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='enable_subsites',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='site',
            name='site',
            field=models.ForeignKey(related_name='sub_sites', blank=True, to='fieldsight.Site', null=True),
        ),
    ]
