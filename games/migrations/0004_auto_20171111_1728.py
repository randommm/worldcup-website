# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20171111_1208'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Predict',
            new_name='Forecast',
        ),
    ]
