# Generated by Django 5.0.4 on 2024-05-01 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='delimeterField',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
