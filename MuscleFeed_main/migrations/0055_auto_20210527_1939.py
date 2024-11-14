# Generated by Django 3.1.2 on 2021-05-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0054_auto_20210527_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='sale_he',
        ),
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='sale_ru',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='no_sale',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='no_sale_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='no_sale_ru',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_1',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_14',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_2',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_4',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='order_sale_6',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='sale_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='sale_ru',
        ),
        migrations.AlterField(
            model_name='menu',
            name='days4_price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='4 дня цена'),
        ),
    ]