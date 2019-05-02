# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0076_auto_20190502_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.ForeignKey(verbose_name='Type of Project', blank=True, to='fieldsight.ProjectType', null=True),
        ),
    ]
