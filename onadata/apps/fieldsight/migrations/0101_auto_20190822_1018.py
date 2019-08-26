# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0100_auto_20190815_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='blueprints',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='blueprints',
            name='doc_type',
            field=models.CharField(default='Drawing', max_length=30, null=True, blank=True, choices=[('Drawing', 'Drawing'), ('Permit', 'Permit'), ('Registration', 'Registration'), ('Identification', 'Identification'), ('Report', 'Report'), ('Contract', 'Contract'), ('Variation', 'Variation'), ('Manual or Instruction', 'Manual or Instruction'), ('Payment or Invoice', 'Payment or Invoice'), ('Notes', 'Notes'), ('Other', 'Other')]),
        ),
        migrations.AddField(
            model_name='blueprints',
            name='name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
