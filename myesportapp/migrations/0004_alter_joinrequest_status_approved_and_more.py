# Generated by Django 4.2.13 on 2024-07-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myesportapp', '0003_remove_joinrequest_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinrequest',
            name='status_approved',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='joinrequest',
            name='status_pending',
            field=models.BooleanField(null=True),
        ),
    ]
