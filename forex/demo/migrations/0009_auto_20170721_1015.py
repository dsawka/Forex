# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0008_auto_20170721_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealmodel',
            name='open_or_closed',
            field=models.CharField(choices=[('Open', 'OPEN'), ('Closed', 'CLOSED')], default='Open', max_length=16),
        ),
    ]
