# Generated by Django 4.1.7 on 2023-12-10 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("UmbrellaApp", "0011_coupon_available"),
    ]

    operations = [
        migrations.AddField(
            model_name="alarm",
            name="site_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="UmbrellaApp.site",
            ),
        ),
        migrations.AlterField(
            model_name="alarm",
            name="alarm_type_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="UmbrellaApp.alarmtype",
            ),
        ),
        migrations.AlterField(
            model_name="alarm",
            name="umbrella_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="UmbrellaApp.umbrella",
            ),
        ),
        migrations.AlterField(
            model_name="alarm",
            name="user_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]