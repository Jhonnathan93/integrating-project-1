# Generated by Django 4.2.4 on 2023-09-14 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_remove_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
