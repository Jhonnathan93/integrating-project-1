# Generated by Django 4.2.4 on 2023-10-17 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isbn", models.CharField(default="N/A", max_length=13)),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(max_length=500)),
                ("year_publication", models.IntegerField(default=0)),
                ("topics", models.CharField(default="N/A", max_length=120)),
                ("rating", models.FloatField(default=0)),
                ("cover", models.URLField()),
                (
                    "buy_link",
                    models.URLField(
                        default="https://books.google.com.co/books?uid=117901420878484918404&hl=es"
                    ),
                ),
                ("author", models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Reader",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(default="", max_length=40)),
                ("password", models.CharField(default="j7531594862", max_length=30)),
                (
                    "email",
                    models.EmailField(default="example@example.com", max_length=50),
                ),
                ("age", models.SmallIntegerField(default=0)),
                ("gender", models.CharField(default="Otro", max_length=40)),
                ("points", models.IntegerField(default=0)),
                (
                    "profile_pic",
                    models.CharField(
                        default="https://i.pinimg.com/280x280_RS/42/03/a5/4203a57a78f6f1b1cc8ce5750f614656.jpg",
                        max_length=100,
                    ),
                ),
            ],
        ),
    ]
