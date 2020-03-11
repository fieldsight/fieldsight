# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0109_userinvite_super_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinvite',
            name='organization',
            field=models.ForeignKey(related_name='invite_organization_roles', blank=True, to='fieldsight.Organization', null=True),
        ),
    ]
