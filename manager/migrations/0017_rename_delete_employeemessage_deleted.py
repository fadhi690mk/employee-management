# Generated by Django 4.2.7 on 2023-11-30 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_employeemessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeemessage',
            old_name='delete',
            new_name='deleted',
        ),
    ]