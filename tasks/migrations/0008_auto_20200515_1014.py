# Generated by Django 3.0.5 on 2020-05-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20200514_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task_category',
            field=models.CharField(max_length=200, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_details',
            field=models.CharField(max_length=500, verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_label',
            field=models.CharField(max_length=200, null=True, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_status',
            field=models.CharField(choices=[('Open', 'Open'), ('Done', 'Done'), ('In Progress', 'In Progress'), ('Deleted', 'Deleted')], default='Open', max_length=100),
        ),
    ]