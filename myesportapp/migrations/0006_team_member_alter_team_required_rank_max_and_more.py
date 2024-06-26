# Generated by Django 4.2.13 on 2024-05-25 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myesportapp', '0005_game_rank2'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='required_rank_max',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='required_rank_min',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
