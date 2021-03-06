# Generated by Django 3.2.3 on 2021-05-26 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20210526_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='week1',
            field=models.CharField(blank=True, choices=[('yet', 'yet'), ('attend', 'attend'), ('absent', 'absent')], default='yet', max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='week2',
            field=models.CharField(blank=True, choices=[('yet', 'yet'), ('attend', 'attend'), ('absent', 'absent')], default='yet', max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='week3',
            field=models.CharField(blank=True, choices=[('yet', 'yet'), ('attend', 'attend'), ('absent', 'absent')], default='yet', max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='week4',
            field=models.CharField(blank=True, choices=[('yet', 'yet'), ('attend', 'attend'), ('absent', 'absent')], default='yet', max_length=100),
        ),
    ]
