# Generated by Django 4.2.7 on 2023-12-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_workreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientnumber',
            name='status',
            field=models.CharField(blank=True, choices=[('interested', 'Interested'), ('not_interested', 'Not Interested'), ('no_response', 'No Response'), ('hold', 'Hold'), (None, 'Null')], default=None, max_length=20),
        ),
    ]
