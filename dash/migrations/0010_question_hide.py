# Generated by Django 4.0.5 on 2022-12-15 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0009_alter_question_content_alter_question_voter'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='hide',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
