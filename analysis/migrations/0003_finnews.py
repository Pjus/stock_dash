# Generated by Django 4.1.5 on 2023-01-17 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0002_financialevent_forecast_financialevent_previous"),
    ]

    operations = [
        migrations.CreateModel(
            name="FinNews",
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
                ("press", models.CharField(default="", max_length=10)),
                ("title", models.CharField(default="", max_length=50)),
                ("url", models.CharField(default="", max_length=100)),
                ("date", models.CharField(default="", max_length=20)),
            ],
        ),
    ]
