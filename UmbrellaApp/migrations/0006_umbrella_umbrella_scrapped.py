# Generated by Django 4.1.7 on 2023-12-06 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UmbrellaApp", "0005_alter_repair_repair_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="umbrella",
            name="umbrella_scrapped",
            field=models.BooleanField(default=False, verbose_name="是否报废"),
        ),
    ]
