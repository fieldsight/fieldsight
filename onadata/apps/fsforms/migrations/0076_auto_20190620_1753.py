# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0008_auto_20190418_1608'),
        ('fsforms', '0075_sharedfieldsightform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedfieldsightform',
            name='fxf',
        ),
        migrations.AddField(
            model_name='sharedfieldsightform',
            name='xf',
            field=models.OneToOneField(null=True, to='logger.XForm'),
        ),
    ]
