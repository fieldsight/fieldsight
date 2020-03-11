# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0108_remove_superorganization_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinvite',
            name='super_organization',
            field=models.ForeignKey(related_name='invite_super_organization_roles', blank=True, to='fieldsight.SuperOrganization', null=True),
        ),
    ]
