# Generated by Django 3.0.5 on 2020-05-13 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200513_1038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='completed_at',
            new_name='completed_time',
        ),
        migrations.RenameField(
            model_name='tasks',
            old_name='created_at',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='tasks',
            old_name='updated_at',
            new_name='last_updated_time',
        ),
    ]
