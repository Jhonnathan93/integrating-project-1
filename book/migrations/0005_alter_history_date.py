# Generated by Django 4.2.1 on 2023-10-18 00:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_history_date_alter_history_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]