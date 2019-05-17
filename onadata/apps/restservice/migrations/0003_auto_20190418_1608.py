# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0002_add_related_name_with_delete_on_cascade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restservice',
            name='name',
            field=models.CharField(max_length=50, choices=[('f2dhis2', 'f2dhis2'), ('bamboo', 'bamboo'), ('generic_xml', 'XML POST'), ('generic_json', 'JSON POST'), ('kpi_hook', 'KPI Hook POST')]),
        ),
    ]
