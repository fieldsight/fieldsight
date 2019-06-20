# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0074_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedFieldSightForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shared', models.BooleanField(default=False)),
                ('fxf', models.OneToOneField(to='fsforms.FieldSightXF')),
            ],
        ),
    ]
