# Generated by Django 4.1.5 on 2023-01-18 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0009_alter_mailingticker_ticker"),
    ]

    operations = [
        migrations.RenameField(
            model_name="stockcompany",
            old_name="recommandtion",
            new_name="recommandation",
        ),
    ]
