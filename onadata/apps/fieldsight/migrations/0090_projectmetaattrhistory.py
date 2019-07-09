# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0089_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMetaAttrHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_attributes', jsonfield.fields.JSONField(default={})),
                ('date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(related_name='meta_history', to='fieldsight.Project')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
