# Generated by Django 4.1.3 on 2023-02-01 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instalacion',
            name='hora',
            field=models.IntegerField(blank=True, choices=[[0, '08:00'], [1, '08:30'], [2, '09:00'], [3, '09:30'], [4, '10:00'], [5, '10:30'], [6, '11:00'], [7, '11:30'], [8, '12:00'], [9, '12:30'], [10, '13:00'], [11, '13:30'], [12, '14:00'], [13, '14:30'], [14, '15:00'], [15, '15:30'], [16, '16:00'], [17, '16:30'], [18, '17:00'], [19, '17:30'], [20, '18:00'], [21, '18:30'], [22, '19:00'], [23, '19:30']], null=True, verbose_name='Hora'),
        ),
    ]
