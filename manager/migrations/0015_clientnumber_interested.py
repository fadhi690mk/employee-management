# Generated by Django 4.2.7 on 2023-11-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_clientnumber_remove'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientnumber',
            name='interested',
            field=models.BooleanField(default=False),
        ),
    ]