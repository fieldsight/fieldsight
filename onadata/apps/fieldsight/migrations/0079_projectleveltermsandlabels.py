# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0078_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLevelTermsAndLabels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('donor', models.CharField(max_length=255)),
                ('site', models.CharField(max_length=255)),
                ('site_supervisor', models.CharField(max_length=255)),
                ('site_reviewer', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('region_supervisor', models.CharField(max_length=255)),
                ('region_reviewer', models.CharField(max_length=255)),
                ('project', models.OneToOneField(related_name='terms_and_labels', to='fieldsight.Project')),
            ],
        ),
    ]
