# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-22 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summaries', '0016_auto_20180122_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='is_bene_experiment',
            field=models.BooleanField(default=False),
        ),
    ]
