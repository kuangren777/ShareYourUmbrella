# Generated by Django 4.1.7 on 2023-12-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UmbrellaApp", "0003_alter_sitestorage_site_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitestorage",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
