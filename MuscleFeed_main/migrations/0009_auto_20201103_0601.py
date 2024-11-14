# Generated by Django 3.1.2 on 2020-11-03 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0008_auto_20201102_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountpagesettings',
            name='comfort_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Comfort Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='easy_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Easy Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='express_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Express Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='gain_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Gain план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='titan_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Titan план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='vegan_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='images/plans/account/', verbose_name='Vegan план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(help_text='Рекомендуемо 720x530, формат webp', upload_to='images/dishes/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='icon',
            field=models.ImageField(blank=True, help_text='Рекомендуемо: 180x180, формат png', null=True, upload_to='icons', verbose_name='Иконка сайта'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan1_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='images/plans/', verbose_name='Фоновое изображение плана 1'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan2_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='images/plans/', verbose_name='Фоновое изображение плана 2'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan3_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='images/plans/', verbose_name='Фоновое изображение плана 3'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan4_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='images/plans/', verbose_name='Фоновое изображение плана 4'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_1',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='images/slider/', verbose_name='Изображение для главного слайдера №1'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_2',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='images/slider/', verbose_name='Изображение для главного слайдера №2'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_3',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='images/slider/', verbose_name='Изображение для главного слайдера №3'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_4',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='images/slider/', verbose_name='Изображение для главного слайдера №4'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_5',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='images/slider/', verbose_name='Изображение для главного слайдера №5'),
        ),
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ImageField(blank=True, help_text='Рекомендуемо: 200x200, формат webp', null=True, upload_to='images/comments/', verbose_name='Фото автора отзыва'),
        ),
    ]
