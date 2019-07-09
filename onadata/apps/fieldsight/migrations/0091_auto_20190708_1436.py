# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0090_projectmetaattrhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmetaattrhistory',
            name='meta_attributes',
        ),
        migrations.AddField(
            model_name='projectmetaattrhistory',
            name='deleted_key_value',
            field=jsonfield.fields.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='projectmetaattrhistory',
            name='new_key_value',
            field=jsonfield.fields.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='projectmetaattrhistory',
            name='old_meta_attributes',
            field=jsonfield.fields.JSONField(default=list),
        ),
    ]
