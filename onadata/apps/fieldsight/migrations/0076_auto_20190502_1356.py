# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0075_auto_20190502_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sub_sector',
            field=models.ForeignKey(related_name='project_sub_sector', verbose_name='Sub-Sector', blank=True, to='fieldsight.Sector', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='sector',
            field=models.ForeignKey(related_name='project_sector', verbose_name='Sector', blank=True, to='fieldsight.Sector', null=True),
        ),
    ]
