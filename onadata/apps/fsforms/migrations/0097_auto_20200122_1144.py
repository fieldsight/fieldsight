# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0112_auto_20200121_1629'),
        ('fsforms', '0096_auto_20200120_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='finstance',
            name='team',
            field=models.ForeignKey(related_name='team_instances', blank=True, to='fieldsight.Organization', null=True),
        ),
        migrations.AddField(
            model_name='finstance',
            name='team_fxf',
            field=models.ForeignKey(related_name='team_form_instances', blank=True, to='fsforms.FieldSightXF', null=True),
        ),
    ]
