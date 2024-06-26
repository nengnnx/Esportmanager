# Generated by Django 4.2.13 on 2024-05-24 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myesportapp', '0003_game_rank_team_game_ranks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='ranks',
        ),
        migrations.AddField(
            model_name='game',
            name='rank1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank5',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank6',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank7',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank8',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rank9',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='number_of_players',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='additional_details',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myesportapp.game'),
        ),
        migrations.AlterField(
            model_name='team',
            name='members_needed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='required_rank_max',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='required_rank_min',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workpicture',
            name='image',
            field=models.ImageField(null=True, upload_to='work_pictures/'),
        ),
        migrations.AlterField(
            model_name='workpicture',
            name='player_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_pictures', to='myesportapp.playerprofile'),
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]
