# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0094_projectmetaattrhistory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='donor',
            field=models.CharField(default='Donor', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='region',
            field=models.CharField(default='Region', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='region_reviewer',
            field=models.CharField(default='Region Reviewer', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='region_supervisor',
            field=models.CharField(default='Region Supervisor', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='site',
            field=models.CharField(default='Site', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='site_reviewer',
            field=models.CharField(default='Site Reviewer', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectleveltermsandlabels',
            name='site_supervisor',
            field=models.CharField(default='Site Supervisor', max_length=255),
        ),
    ]
