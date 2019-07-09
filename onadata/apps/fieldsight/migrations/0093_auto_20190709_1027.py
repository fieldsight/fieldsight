# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0092_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectmetaattrhistory',
            old_name='deleted_key_value',
            new_name='new_meta_atrributes',
        ),
        migrations.RemoveField(
            model_name='projectmetaattrhistory',
            name='new_key_value',
        ),
    ]
