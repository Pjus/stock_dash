# Generated by Django 4.1.4 on 2022-12-28 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_portfolio_monthly_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('buy_price', models.FloatField(default=0.0)),
                ('sell_price', models.FloatField(default=0.0)),
                ('buy_date', models.DateField(blank=True, null=True)),
                ('sell_date', models.DateField(blank=True, null=True)),
                ('profit', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='monthly_return',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='port_history',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
