# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0112_auto_20200121_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinvite',
            name='teams',
            field=models.ManyToManyField(related_name='invite_team_roles', to='fieldsight.Organization'),
        ),
    ]
