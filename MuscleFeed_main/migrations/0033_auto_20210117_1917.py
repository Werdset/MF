# Generated by Django 3.1.2 on 2021-01-17 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0032_fixed_notification_mails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='excluding_weekday',
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='change_menu',
            field=models.CharField(default='Выбрать другое меню', max_length=200, verbose_name='Выбрать другое меню'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='change_menu_he',
            field=models.CharField(default='Выбрать другое меню', max_length=200, null=True, verbose_name='Выбрать другое меню'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='change_menu_ru',
            field=models.CharField(default='Выбрать другое меню', max_length=200, null=True, verbose_name='Выбрать другое меню'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='meal_days',
            field=models.CharField(default='Дней питания:', max_length=200, verbose_name='Дней питания:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='meal_days_he',
            field=models.CharField(default='Дней питания:', max_length=200, null=True, verbose_name='Дней питания:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='meal_days_ru',
            field=models.CharField(default='Дней питания:', max_length=200, null=True, verbose_name='Дней питания:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='we_will_return',
            field=models.CharField(default='Мы вам вернем:', max_length=200, verbose_name='Мы вам вернем:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='we_will_return_he',
            field=models.CharField(default='Мы вам вернем:', max_length=200, null=True, verbose_name='Мы вам вернем:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='we_will_return_ru',
            field=models.CharField(default='Мы вам вернем:', max_length=200, null=True, verbose_name='Мы вам вернем:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='you_need_to_pay',
            field=models.CharField(default='Необходимо доплатить:', max_length=200, verbose_name='Необходимо доплатить:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='you_need_to_pay_he',
            field=models.CharField(default='Необходимо доплатить:', max_length=200, null=True, verbose_name='Необходимо доплатить:'),
        ),
        migrations.AddField(
            model_name='accountpagesettings',
            name='you_need_to_pay_ru',
            field=models.CharField(default='Необходимо доплатить:', max_length=200, null=True, verbose_name='Необходимо доплатить:'),
        ),
        migrations.AddField(
            model_name='order',
            name='changed_menu',
            field=models.BooleanField(default=False, editable=False, verbose_name='Измененное меню'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_return',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Вернуть'),
        ),
    ]
