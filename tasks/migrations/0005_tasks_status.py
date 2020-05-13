# Generated by Django 3.0.5 on 2020-05-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200513_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Open'), (1, 'Done'), (2, 'Progress'), (3, 'Deleted')], default=0),
        ),
    ]
