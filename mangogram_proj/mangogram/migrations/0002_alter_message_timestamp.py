# Generated by Django 5.0.6 on 2024-05-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangogram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.IntegerField(),
        ),
    ]