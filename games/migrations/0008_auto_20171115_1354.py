# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20171113_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='prob1',
            new_name='prob0',
        ),
        migrations.RenameField(
            model_name='forecast',
            old_name='prob1',
            new_name='prob0',
        ),
    ]
