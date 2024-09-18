# Generated by Django 5.0.7 on 2024-09-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0017_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2),
        ),
    ]
