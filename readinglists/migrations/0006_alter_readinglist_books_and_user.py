# Generated manually to match the model refactor.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("readinglists", "0005_alter_readinglist_cover"),
    ]

    operations = [
        migrations.AlterField(model_name="readinglist", name="books", field=models.ManyToManyField(blank=True, to="book.book")),
        migrations.AlterField(model_name="readinglist", name="user", field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
    ]
