# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0074_site_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Team Name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Type of Team', blank=True, to='fieldsight.OrganizationType', null=True),
        ),
    ]
