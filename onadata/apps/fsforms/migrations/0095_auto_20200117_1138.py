# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0094_auto_20200107_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldsightxf',
            name='organization_form_lib',
            field=models.ForeignKey(related_name='organization_forms', blank=True, to='fsforms.OrganizationFormLibrary', null=True),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='is_form_library',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='schedule',
            name='organization_form_lib',
            field=models.ForeignKey(related_name='schedules', blank=True, to='fsforms.OrganizationFormLibrary', null=True),
        ),
        migrations.AlterField(
            model_name='finstance',
            name='project_fxf',
            field=models.ForeignKey(related_name='project_form_instances', blank=True, to='fsforms.FieldSightXF', null=True),
        ),
    ]
