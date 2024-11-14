# Generated by Django 3.1.2 on 2020-12-26 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0025_auto_20201225_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountpagesettings',
            name='active_fit_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Active Fit план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='balance_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Balance план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='comfort_fit_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Comfort Fit план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='express_fit_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Express Fit план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='titan_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Titan план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='vegetarian_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='', verbose_name='Vegetarian план фоновое изображение webp'),
        ),
        migrations.AddField(
            model_name='dish',
            name='image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 720x530, формат webp', null=True, upload_to='', verbose_name='Изображение webp'),
        ),
        migrations.AddField(
            model_name='fixed',
            name='logo_webp',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='global/', verbose_name='Логотип сайта webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='plan1_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='', verbose_name='Фоновое изображение плана 1 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='plan2_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='', verbose_name='Фоновое изображение плана 2 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='plan3_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='', verbose_name='Фоновое изображение плана 3 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='plan4_image_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='', verbose_name='Фоновое изображение плана 4 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='slider_image_1_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='', verbose_name='Изображение для главного слайдера №1 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='slider_image_2_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='', verbose_name='Изображение для главного слайдера №2 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='slider_image_3_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='', verbose_name='Изображение для главного слайдера №2 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='slider_image_4_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='', verbose_name='Изображение для главного слайдера №4 webp'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='slider_image_5_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='', verbose_name='Изображение для главного слайдера №5 webp'),
        ),
        migrations.AddField(
            model_name='review',
            name='photo_webp',
            field=models.ImageField(blank=True, editable=False, help_text='Рекомендуемо: 200x200, формат webp', null=True, upload_to='reviews/', verbose_name='Фото автора отзыва webp'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='active_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Active Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='balance_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Balance план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='comfort_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Comfort Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='express_fit_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Express Fit план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='titan_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Titan план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='accountpagesettings',
            name='vegetarian_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='account/plans/', verbose_name='Vegetarian план фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(help_text='Рекомендуемо 720x530, формат webp', upload_to='dishes/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='icon',
            field=models.ImageField(blank=True, help_text='Рекомендуемо: 180x180, формат png', null=True, upload_to='icons/', verbose_name='Иконка сайта'),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='global/', verbose_name='Логотип сайта'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='delivery_map',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='homepage/maps/', verbose_name='Карта доставки'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='delivery_map_he',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='homepage/maps/', verbose_name='Карта доставки'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='delivery_map_ru',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 800x600, формат webp', null=True, upload_to='homepage/maps/', verbose_name='Карта доставки'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='open_graph_image',
            field=models.ImageField(blank=True, help_text='Используется в SEO', null=True, upload_to='homepage/', verbose_name='Open Graph image'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='open_graph_image_he',
            field=models.ImageField(blank=True, help_text='Используется в SEO', null=True, upload_to='homepage/', verbose_name='Open Graph image'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='open_graph_image_ru',
            field=models.ImageField(blank=True, help_text='Используется в SEO', null=True, upload_to='homepage/', verbose_name='Open Graph image'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan1_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='homepage/plans/', verbose_name='Фоновое изображение плана 1'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan2_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='homepage/plans/', verbose_name='Фоновое изображение плана 2'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan3_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='homepage/plans/', verbose_name='Фоновое изображение плана 3'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='plan4_image',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 920x1000, формат webp', null=True, upload_to='homepage/plans/', verbose_name='Фоновое изображение плана 4'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_1',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='homepage/slider/', verbose_name='Изображение для главного слайдера №1'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_2',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='homepage/slider/', verbose_name='Изображение для главного слайдера №2'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_3',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='homepage/slider/', verbose_name='Изображение для главного слайдера №3'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_4',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='homepage/slider/', verbose_name='Изображение для главного слайдера №3'),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='slider_image_5',
            field=models.ImageField(blank=True, help_text='Рекомендуемо 4096x3072, формат webp', null=True, upload_to='homepage/slider/', verbose_name='Изображение для главного слайдера №5'),
        ),
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ImageField(blank=True, help_text='Рекомендуемо: 200x200, формат webp', null=True, upload_to='reviews/', verbose_name='Фото автора отзыва'),
        ),
    ]
