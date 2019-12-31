# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0108_remove_superorganization_type'),
        ('userrole', '0005_auto_20190425_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='super_organization',
            field=models.ForeignKey(related_name='super_organization_roles', blank=True, to='fieldsight.SuperOrganization', null=True),
        ),
    ]
