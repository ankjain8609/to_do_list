# Generated by Django 3.0.6 on 2020-05-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_auto_20200523_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskloghours',
            name='task_time_spent',
            field=models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Task Time Spent'),
        ),
    ]