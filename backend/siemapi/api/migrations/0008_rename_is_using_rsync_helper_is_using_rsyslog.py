# Generated by Django 5.0.4 on 2024-06-06 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_alert_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='helper',
            old_name='is_using_rsync',
            new_name='is_using_rsyslog',
        ),
    ]
