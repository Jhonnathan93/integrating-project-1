# Generated by Django 4.2.4 on 2023-09-14 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
    ]