# Generated by Django 4.1.5 on 2023-01-17 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0005_stockcompany_recommandtion"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockIndex",
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
                ("ticker", models.CharField(default="", max_length=5)),
                ("index_name", models.CharField(default="", max_length=20)),
            ],
        ),
    ]
