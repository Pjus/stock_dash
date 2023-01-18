# Generated by Django 4.1.5 on 2023-01-18 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0010_rename_recommandtion_stockcompany_recommandation"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailingticker",
            name="company",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailing_company",
                to="analysis.stockcompany",
            ),
        ),
        migrations.AlterField(
            model_name="mailingticker",
            name="ticker",
            field=models.CharField(default="", max_length=10),
        ),
    ]
