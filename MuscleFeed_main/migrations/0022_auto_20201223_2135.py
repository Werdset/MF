# Generated by Django 3.1.2 on 2020-12-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0021_auto_20201223_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagesettings',
            name='select',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='select_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='select_ru',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='selected',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='selected_he',
        ),
        migrations.RemoveField(
            model_name='homepagesettings',
            name='selected_ru',
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select_sex',
            field=models.CharField(default='Выберие пол:', max_length=200, verbose_name='Выберие пол:'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select_sex_he',
            field=models.CharField(default='Выберие пол:', max_length=200, null=True, verbose_name='Выберие пол:'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='select_sex_ru',
            field=models.CharField(default='Выберие пол:', max_length=200, null=True, verbose_name='Выберие пол:'),
        ),
    ]