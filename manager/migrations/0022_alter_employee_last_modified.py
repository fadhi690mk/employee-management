# Generated by Django 4.2.7 on 2023-12-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_employee_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='last_modified',
            field=models.DateTimeField(blank=True),
        ),
    ]
