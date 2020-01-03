# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0108_remove_superorganization_type'),
        ('eventlog', '0062_auto_20191223_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldsightlog',
            name='super_organization',
            field=models.ForeignKey(related_name='logs', blank=True, to='fieldsight.SuperOrganization', null=True),
        ),
    ]
