# Generated by Django 3.1.2 on 2020-12-24 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0022_auto_20201223_2135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'ordering': ['admin_name'], 'verbose_name': 'Блюдо', 'verbose_name_plural': 'Блюда'},
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select',
            field=models.CharField(default='Выбрать', max_length=200, verbose_name='Выбрать'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select_he',
            field=models.CharField(default='Выбрать', max_length=200, null=True, verbose_name='Выбрать'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select_ru',
            field=models.CharField(default='Выбрать', max_length=200, null=True, verbose_name='Выбрать'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='completed_pl',
            field=models.CharField(default='Завершенные', max_length=200, verbose_name='Завершенные'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='completed_pl_he',
            field=models.CharField(default='Завершенные', max_length=200, null=True, verbose_name='Завершенные'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='completed_pl_ru',
            field=models.CharField(default='Завершенные', max_length=200, null=True, verbose_name='Завершенные'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='select_sex',
            field=models.CharField(default='Выберите пол:', max_length=200, verbose_name='Выберите пол:'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='select_sex_he',
            field=models.CharField(default='Выберите пол:', max_length=200, null=True, verbose_name='Выберите пол:'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='select_sex_ru',
            field=models.CharField(default='Выберите пол:', max_length=200, null=True, verbose_name='Выберите пол:'),
        ),
    ]