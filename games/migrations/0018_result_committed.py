# Generated by Django 2.0 on 2017-12-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_auto_20171207_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='committed',
            field=models.BooleanField(default=False),
        ),
    ]