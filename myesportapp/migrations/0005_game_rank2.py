# Generated by Django 4.2.13 on 2024-05-24 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myesportapp', '0004_remove_game_ranks_game_rank1_game_rank3_game_rank4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='rank2',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
