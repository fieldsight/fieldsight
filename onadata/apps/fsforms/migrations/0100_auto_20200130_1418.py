# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0099_auto_20200130_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finstance',
            name='organization_fxf',
        ),
        migrations.AddField(
            model_name='finstance',
            name='organization_form_lib',
            field=models.ForeignKey(related_name='organization_form_instances', blank=True, to='fsforms.OrganizationFormLibrary', null=True),
        ),
    ]
