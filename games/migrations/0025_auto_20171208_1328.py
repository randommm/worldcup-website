# Generated by Django 2.0 on 2017-12-08 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0024_auto_20171208_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
