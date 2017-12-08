# Generated by Django 2.0 on 2017-12-08 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0025_auto_20171208_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leagueuser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='point',
            name='id',
        ),
        migrations.RemoveField(
            model_name='result',
            name='id',
        ),
        migrations.AlterField(
            model_name='leagueuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='point',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='result',
            name='game',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='games.Game'),
        ),
    ]