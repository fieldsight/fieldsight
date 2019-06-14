# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_auto_20190415_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackPeriodicWarningEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_email_send', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('subscriber', models.ForeignKey(related_name='periodic_warning_email', to='subscriptions.Subscription')),
            ],
        ),
    ]
