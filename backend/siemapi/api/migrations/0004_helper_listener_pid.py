# Generated by Django 5.0.4 on 2024-05-08 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_helper'),
    ]

    operations = [
        migrations.AddField(
            model_name='helper',
            name='listener_pid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
