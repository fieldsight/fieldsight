# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0100_auto_20200130_1418'),
        ('viewer', '0006_export_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='export',
            name='organization_form_lib',
            field=models.ForeignKey(related_name='exports', blank=True, to='fsforms.OrganizationFormLibrary', null=True),
        ),
    ]
