# Generated by Django 4.2.4 on 2023-11-07 02:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0007_book_disliked_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
