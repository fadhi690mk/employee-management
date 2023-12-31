# Generated by Django 4.2.7 on 2023-11-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_workdone_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='extraWork',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='monthlyDone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='monthlyPending',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='totalWork',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='weeklyDone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='weeklyPending',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Workdone',
        ),
    ]
