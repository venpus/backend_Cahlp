# Generated by Django 4.1.11 on 2023-09-11 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_rename_date_joined_device_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicedata',
            old_name='date_joined',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='otaupdate',
            old_name='date_joined',
            new_name='created_at',
        ),
    ]
