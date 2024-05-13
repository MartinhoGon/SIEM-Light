# Generated by Django 5.0.4 on 2024-05-13 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_helper_listener_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='helper',
            name='is_sniffer_running',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='helper',
            name='sniffer_pid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
