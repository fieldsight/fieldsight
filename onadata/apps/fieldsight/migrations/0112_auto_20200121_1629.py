# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0111_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='identifier',
            field=models.CharField(max_length=255, null=True, verbose_name='ID', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='identifier',
            field=models.CharField(max_length=255, null=True, verbose_name='ID', blank=True),
        ),
        migrations.AddField(
            model_name='superorganization',
            name='identifier',
            field=models.CharField(max_length=255, null=True, verbose_name='ID', blank=True),
        ),
    ]
