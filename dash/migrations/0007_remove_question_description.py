# Generated by Django 4.0.2 on 2022-12-10 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0006_question_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='description',
        ),
    ]
