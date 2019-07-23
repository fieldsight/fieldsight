# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0096_auto_20190717_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMetaAttrAnsHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_attributes_ans', jsonfield.fields.JSONField(default={})),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(blank=True, null=True, choices=[(1, 'By submission'), (2, 'By change in meta attributes')])),
                ('site', models.ForeignKey(related_name='meta_history', to='fieldsight.Site')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.RemoveField(
            model_name='sitemetaattrhistory',
            name='site',
        ),
        migrations.DeleteModel(
            name='SiteMetaAttrHistory',
        ),
    ]
