# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0097_auto_20190719_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='logo',
            field=models.ImageField(default='logo/default_site_image.png', max_length=500, upload_to='logo'),
        ),
    ]
