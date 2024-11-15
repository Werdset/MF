# Generated by Django 3.1.2 on 2021-09-24 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0058_auto_20210822_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_28',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_28_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_28_ru',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='day27',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='day27_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='day28',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='day28_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='days28_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_day27',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_day28',
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_26',
            field=models.CharField(default='26 дней питания', max_length=200, verbose_name='26 дней питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_26_he',
            field=models.CharField(default='26 дней питания', max_length=200, null=True, verbose_name='26 дней питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_26_ru',
            field=models.CharField(default='26 дней питания', max_length=200, null=True, verbose_name='26 дней питания'),
        ),
        migrations.AddField(
            model_name='menu',
            name='days26_price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='26 дней цена'),
        ),
    ]
