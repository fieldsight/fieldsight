# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0070_auto_20190520_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditedSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new', models.ForeignKey(related_name='new_edits', to='fsforms.FInstance')),
                ('old', models.ForeignKey(related_name='edits', to='fsforms.FInstance')),
            ],
        ),
    ]
