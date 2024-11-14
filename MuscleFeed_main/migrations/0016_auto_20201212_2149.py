# Generated by Django 3.1.2 on 2020-12-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0015_auto_20201211_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='calories',
            field=models.IntegerField(verbose_name='Калории (в мужской версии)'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='carbohydrates',
            field=models.IntegerField(verbose_name='Углеводы (в мужской версии)'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='fats',
            field=models.IntegerField(verbose_name='Жиры (в мужской версии)'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='proteins',
            field=models.IntegerField(verbose_name='Белки (в мужской версии)'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='weight',
            field=models.IntegerField(verbose_name='Вес в граммах (в мужской версии)'),
        ),
    ]