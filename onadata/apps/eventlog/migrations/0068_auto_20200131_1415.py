# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0067_auto_20200131_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celerytaskprogress',
            name='task_type',
            field=models.IntegerField(default=0, choices=[(0, 'Bulk Site Update'), (1, 'User Assign to Project'), (2, 'User Assign to Site'), (3, 'Site Response Xls Report'), (4, 'Site Import'), (6, 'Zip Site Images'), (7, 'Remove Roles'), (8, 'Site Data Export'), (9, 'Response Pdf Report'), (10, 'Site Progress Xls Report'), (11, 'Project Statstics Report'), (12, 'Log Report'), (13, 'User Assign to Region'), (14, 'User Assign to an entire project'), (15, 'Auto Clone and Deploy General Form'), (16, 'User Activity Xls Report'), (17, 'Share XForm'), (18, 'Share XForm to Created Manager'), (19, 'Share XForm to Individuals'), (20, 'Share XForm to Project Managers and Admin of Project'), (21, 'Share XForm to team'), (22, 'Clone Form'), (22, 'Update Sites Progress'), (23, 'Update Site Progress'), (24, 'Update and Create History of Site Meta-attributes Answers'), (25, 'Update Site Information on Submission'), (26, 'Export Report in excel'), (27, 'Add default forms in Projects'), (28, 'Remove default forms from Organization'), (28, 'Remove team from Organization')]),
        ),
    ]
