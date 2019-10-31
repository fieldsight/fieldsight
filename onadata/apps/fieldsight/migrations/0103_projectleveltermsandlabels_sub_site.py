# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0102_site_all_ma_ans'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectleveltermsandlabels',
            name='sub_site',
            field=models.CharField(default='Subsite', max_length=255),
        ),
    ]
