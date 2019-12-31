# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0008_auto_20190418_1608'),
        ('fieldsight', '0108_remove_superorganization_type'),
        ('fsforms', '0091_auto_20191210_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationFormLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='library_forms', to='fieldsight.SuperOrganization')),
                ('xf', models.ForeignKey(related_name='library_forms', to='logger.XForm')),
            ],
        ),
    ]
