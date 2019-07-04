# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0018_auto_20190703_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='IdPassProof',
            new_name='id_pass_proof',
        ),
    ]
