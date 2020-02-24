# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0113_userinvite_teams'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMapFiltersMetrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_information_filters', jsonfield.fields.JSONField(default=dict)),
                ('form_data_filters', jsonfield.fields.JSONField(default=dict)),
                ('project', models.OneToOneField(to='fieldsight.Project')),
            ],
        ),
    ]
