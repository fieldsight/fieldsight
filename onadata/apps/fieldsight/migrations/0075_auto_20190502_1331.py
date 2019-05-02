# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0074_site_date_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('sector', models.ForeignKey(related_name='sectors', to='fieldsight.Sector', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='sector',
            field=models.ForeignKey(verbose_name='Sector', blank=True, to='fieldsight.Sector', null=True),
        ),
    ]
