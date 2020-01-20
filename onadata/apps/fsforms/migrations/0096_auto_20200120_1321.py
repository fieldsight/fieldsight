# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0111_merge'),
        ('fsforms', '0095_auto_20200117_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='finstance',
            name='organization',
            field=models.ForeignKey(related_name='organization_instances', blank=True, to='fieldsight.SuperOrganization', null=True),
        ),
        migrations.AddField(
            model_name='finstance',
            name='organization_fxf',
            field=models.ForeignKey(related_name='organization_form_instances', blank=True, to='fsforms.FieldSightXF', null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
