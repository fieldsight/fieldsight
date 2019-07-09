# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0082_auto_20190620_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.IntegerField(default=0, choices=[(0, 'Default (stages approved / total stages)'), (1, 'Most advanced approved stage'), (2, 'Pull integer from form'), (3, '# of site submissions (All forms)'), (4, '# of site submissions (for a form)'), (5, 'Manually update')])),
                ('pull_integer_form', models.IntegerField(null=True, blank=True)),
                ('pull_integer_form_question', models.CharField(max_length=31, null=True, blank=True)),
                ('no_submissions_form', models.IntegerField(null=True, blank=True)),
                ('no_submissions_total_count', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(related_name='progress_settings', to='fieldsight.Project')),
            ],
        ),
        migrations.CreateModel(
            name='SiteMetaAttrHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_attributes', jsonfield.fields.JSONField(default=list)),
                ('date', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(related_name='meta_history', to='fieldsight.Site')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='SiteProgressHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(related_name='progress_history', to='fieldsight.Site')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
