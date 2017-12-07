# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_auto_20171115_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='games.Team'),
        ),
    ]