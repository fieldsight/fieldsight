# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0069_auto_20181207_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldsightxf',
            name='schedule',
            field=models.OneToOneField(related_name='schedule_forms', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='fsforms.Schedule'),
        ),
        migrations.AlterField(
            model_name='fieldsightxf',
            name='stage',
            field=models.OneToOneField(related_name='stage_forms', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='fsforms.Stage'),
        ),
    ]
