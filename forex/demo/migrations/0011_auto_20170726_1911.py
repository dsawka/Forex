# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0010_dealmodel_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealmodel',
            name='result',
            field=models.DecimalField(decimal_places=5, max_digits=6, null=True),
        ),
    ]
