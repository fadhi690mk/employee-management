# Generated by Django 4.2.7 on 2023-11-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_clientnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientnumber',
            name='number',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]