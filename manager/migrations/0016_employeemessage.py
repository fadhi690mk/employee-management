# Generated by Django 4.2.7 on 2023-11-30 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_clientnumber_interested'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employeemessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeemessage', models.TextField()),
                ('delete', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.employee')),
            ],
        ),
    ]
