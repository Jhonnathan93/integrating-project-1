# Generated manually to remove the duplicate dislike relation.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0009_rename_date_book_dateadded"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="disliked_by",
        ),
    ]
