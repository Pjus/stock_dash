# Generated by Django 4.0.2 on 2022-12-07 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_remove_portfolio_stocks_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='add_port',
            new_name='portfolio',
        ),
    ]
