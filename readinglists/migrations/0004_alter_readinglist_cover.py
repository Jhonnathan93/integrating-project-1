# Generated by Django 4.2.4 on 2023-10-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readinglists', '0003_alter_readinglist_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinglist',
            name='cover',
            field=models.ImageField(blank=True, default='readinglist/default_cover.jpg', null=True, upload_to='readinglists/covers/'),
        ),
    ]