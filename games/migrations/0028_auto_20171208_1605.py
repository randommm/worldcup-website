# Generated by Django 2.0 on 2017-12-08 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0027_auto_20171208_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_team0_set', to='games.Team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_team1_set', to='games.Team'),
        ),
        migrations.AlterField(
            model_name='leagueuser',
            name='asked_to_join_league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leagueuser_asked_to_join_league_set', to='games.League'),
        ),
        migrations.AlterField(
            model_name='leagueuser',
            name='invited_by_league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leagueuser_invited_by_league_set', to='games.League'),
        ),
        migrations.AlterField(
            model_name='leagueuser',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leagueuser_league_set', to='games.League'),
        ),
    ]
