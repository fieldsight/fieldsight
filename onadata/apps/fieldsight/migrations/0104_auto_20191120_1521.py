# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0103_projectleveltermsandlabels_sub_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='current_progress',
            field=models.FloatField(default=0.0),
        ),
    ]
