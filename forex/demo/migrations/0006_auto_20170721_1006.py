# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0005_dealmodel_open_or_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealmodel',
            name='open_or_closed',
            field=models.CharField(choices=[('OPEN', 'open'), ('CLOSED', 'closed')], default='open', max_length=16),
        ),
    ]
