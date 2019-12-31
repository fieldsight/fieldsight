# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0106_auto_20191219_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superorganization',
            name='owner',
            field=models.ForeignKey(related_name='super_organizations', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
