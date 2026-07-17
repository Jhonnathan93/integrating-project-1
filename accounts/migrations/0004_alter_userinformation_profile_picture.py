# Generated manually to match the model refactor.

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [("accounts", "0003_alter_userinformation_birthdate_and_more")]

    operations = [
        migrations.AlterField(
            model_name="userinformation",
            name="birthdate",
            field=models.DateField(default=timezone.localdate),
        ),
        migrations.AlterField(
            model_name="userinformation",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="accounts/profile_pics/"),
        ),
    ]
