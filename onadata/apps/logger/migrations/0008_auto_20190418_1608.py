# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import onadata.apps.logger.models.attachment
import onadata.apps.logger.fields


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0007_instance_is_synced_with_mongo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='xform',
            options={'ordering': ('id_string',), 'verbose_name': 'XForm', 'verbose_name_plural': 'XForms', 'permissions': (('view_xform', 'Can view associated data'), ('report_xform', 'Can make submissions to the form'), ('move_xform', 'Can move form between projects'), ('transfer_xform', 'Can transfer form ownership.'), ('validate_xform', 'Can validate submissions.'))},
        ),
        migrations.AddField(
            model_name='attachment',
            name='media_file_basename',
            field=models.CharField(db_index=True, max_length=260, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='posted_to_kpi',
            field=onadata.apps.logger.fields.LazyDefaultBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instance',
            name='validation_status',
            field=jsonfield.fields.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='xform',
            name='has_kpi_hooks',
            field=onadata.apps.logger.fields.LazyDefaultBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='media_file',
            field=models.FileField(max_length=380, upload_to=onadata.apps.logger.models.attachment.upload_to, db_index=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='mimetype',
            field=models.CharField(default=b'', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='uuid',
            field=models.CharField(default='', max_length=249, db_index=True),
        ),
        migrations.AlterField(
            model_name='xform',
            name='uuid',
            field=models.CharField(default='', max_length=32, db_index=True),
        ),
    ]
