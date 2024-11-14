# Generated by Django 3.1.2 on 2020-12-12 22:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0016_auto_20201212_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixed',
            name='site_description',
            field=models.CharField(default='Лучший сервис доставки правильного питания.<br>Ешь вкусно. Худей легко!', max_length=1000, verbose_name='Описание сайта'),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='site_description_he',
            field=models.CharField(default='Лучший сервис доставки правильного питания.<br>Ешь вкусно. Худей легко!', max_length=1000, null=True, verbose_name='Описание сайта'),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='site_description_ru',
            field=models.CharField(default='Лучший сервис доставки правильного питания.<br>Ешь вкусно. Худей легко!', max_length=1000, null=True, verbose_name='Описание сайта'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_description',
            field=ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Небольшое описание на слайдере'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_description_he',
            field=ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Небольшое описание на слайдере'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_description_ru',
            field=ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Небольшое описание на слайдере'),
        ),
    ]
