# Generated by Django 3.1.2 on 2020-12-27 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0027_homepagesettings_delivery_map_webp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_3',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_30',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_30_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_30_ru',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_3_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='meal_days_3_ru',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_3',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_30',
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='comment',
            field=models.CharField(default='Комментарий', max_length=200, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='comment_he',
            field=models.CharField(default='Комментарий', max_length=200, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='comment_ru',
            field=models.CharField(default='Комментарий', max_length=200, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_2',
            field=models.CharField(default='2 дня питания', max_length=200, verbose_name='2 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_2_he',
            field=models.CharField(default='2 дня питания', max_length=200, null=True, verbose_name='2 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_2_ru',
            field=models.CharField(default='2 дня питания', max_length=200, null=True, verbose_name='2 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_4',
            field=models.CharField(default='4 дня питания', max_length=200, verbose_name='4 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_4_he',
            field=models.CharField(default='4 дня питания', max_length=200, null=True, verbose_name='4 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='meal_days_4_ru',
            field=models.CharField(default='4 дня питания', max_length=200, null=True, verbose_name='4 дня питания'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='order_sale_2',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=8, verbose_name='Скидка на заказ 2 дня'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='order_sale_4',
            field=models.DecimalField(decimal_places=2, default=12, max_digits=8, verbose_name='Скидка на заказ 4 дня'),
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Комментарий'),
        ),
    ]