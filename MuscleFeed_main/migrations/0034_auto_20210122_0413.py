# Generated by Django 3.1.2 on 2021-01-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0033_auto_20210117_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='friday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='monday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='saturday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='sunday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='thursday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='tuesday_price_male2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_other',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_other2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_price_female',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_price_female2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_price_male',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='wednesday_price_male2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_friday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_friday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_monday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_monday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_saturday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_saturday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_sunday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_sunday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_thursday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_thursday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_tuesday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_tuesday2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_wednesday',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes_wednesday2',
        ),
        migrations.AddField(
            model_name='menu',
            name='day1',
            field=models.ManyToManyField(blank=True, null=True, related_name='day1', to='MuscleFeed_main.Dish', verbose_name='Первый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day10',
            field=models.ManyToManyField(blank=True, null=True, related_name='day10', to='MuscleFeed_main.Dish', verbose_name='Десятый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day10_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day10_other', to='MuscleFeed_main.Dish', verbose_name='Десятый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day10_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Десятый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day10_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Десятый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day11',
            field=models.ManyToManyField(blank=True, null=True, related_name='day11', to='MuscleFeed_main.Dish', verbose_name='Одиннадцатый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day11_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day11_other', to='MuscleFeed_main.Dish', verbose_name='Одиннадцатый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day11_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Одиннадцатый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day11_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Одиннадцатый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day12',
            field=models.ManyToManyField(blank=True, null=True, related_name='day12', to='MuscleFeed_main.Dish', verbose_name='Двенадцатый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day12_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day12_other', to='MuscleFeed_main.Dish', verbose_name='Двенадцатый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day12_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Двенадцатый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day12_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Двенадцатый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day1_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day1_other', to='MuscleFeed_main.Dish', verbose_name='Первый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day1_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Первый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day1_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Первый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day2',
            field=models.ManyToManyField(blank=True, null=True, related_name='day2', to='MuscleFeed_main.Dish', verbose_name='Второй день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day2_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day2_other', to='MuscleFeed_main.Dish', verbose_name='Второй день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day2_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Второй день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day2_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Второй день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day3',
            field=models.ManyToManyField(blank=True, null=True, related_name='day3', to='MuscleFeed_main.Dish', verbose_name='Третий день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day3_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day3_other', to='MuscleFeed_main.Dish', verbose_name='Третий день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day3_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Третий день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day3_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Третий день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day4',
            field=models.ManyToManyField(blank=True, null=True, related_name='day4', to='MuscleFeed_main.Dish', verbose_name='Четвертый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day4_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day4_other', to='MuscleFeed_main.Dish', verbose_name='Четвертый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day4_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Четвертый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day4_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Четвертый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day5',
            field=models.ManyToManyField(blank=True, null=True, related_name='day5', to='MuscleFeed_main.Dish', verbose_name='Пятный день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day5_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day5_other', to='MuscleFeed_main.Dish', verbose_name='Пятный день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day5_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Пятный день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day5_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Пятный день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day6',
            field=models.ManyToManyField(blank=True, null=True, related_name='day6', to='MuscleFeed_main.Dish', verbose_name='Шестой день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day6_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day6_other', to='MuscleFeed_main.Dish', verbose_name='Шестой день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day6_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Шестой день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day6_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Шестой день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day7',
            field=models.ManyToManyField(blank=True, null=True, related_name='day7', to='MuscleFeed_main.Dish', verbose_name='Седьмой день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day7_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day7_other', to='MuscleFeed_main.Dish', verbose_name='Седьмой день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day7_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Седьмой день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day7_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Седьмой день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day8',
            field=models.ManyToManyField(blank=True, null=True, related_name='day8', to='MuscleFeed_main.Dish', verbose_name='Восьмой день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day8_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day8_other', to='MuscleFeed_main.Dish', verbose_name='Восьмой день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day8_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Восьмой день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day8_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Восьмой день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day9',
            field=models.ManyToManyField(blank=True, null=True, related_name='day9', to='MuscleFeed_main.Dish', verbose_name='Девятый день стандартно'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day9_other',
            field=models.ManyToManyField(blank=True, null=True, related_name='day9_other', to='MuscleFeed_main.Dish', verbose_name='Девятый день все блюда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day9_price_female',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Девятый день цена (в женской версии)'),
        ),
        migrations.AddField(
            model_name='menu',
            name='day9_price_male',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8, verbose_name='Девятый день цена (в мужской версии)'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day1',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day1', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда первый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day10',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day10', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда десятый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day11',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day11', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда одиннадцатый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day12',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day12', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда двенадцатый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day2',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day2', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда второй день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day3',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day3', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда третий день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day4',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day4', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда четвертый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day5',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day5', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда пятый день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day6',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day6', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда шестой день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day7',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day7', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда седьмой день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day8',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day8', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда восьмой день'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes_day9',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes_day9', to='MuscleFeed_main.Dish', verbose_name='Выбранные блюда девятый день'),
        ),
    ]
