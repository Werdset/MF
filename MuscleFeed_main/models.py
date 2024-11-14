import datetime
import os
import random
from decimal import Decimal
from io import BytesIO

from PIL import Image
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from MuscleFeed_settings import settings


def add_webp_image(image_field, image_webp_field):
    img = Image.open(image_field.file.file)
    buffer = BytesIO()
    img.save(buffer, format='WEBP', losseless=False, quality=80, method=6)
    image_webp_field.save(
        image_field.name[:-4] + '.webp',
        InMemoryUploadedFile(
            buffer,
            None, '',
            'image/webp',
            img.size,
            None,
        ),
        save=False
    )


class Fixed(models.Model):
    """ Глобальные настройки """
    icon = models.ImageField('Иконка сайта', help_text='Рекомендуемо: 180x180, формат png', upload_to='icons/',
                             null=True,
                             blank=True)
    logo = models.ImageField('Логотип сайта', upload_to='global/', null=True, blank=True)
    logo_webp = models.ImageField('Логотип сайта webp', upload_to='global/', null=True, blank=True, editable=False)
    site_name = models.CharField('Название сайта', help_text='Google', max_length=50, default='')
    site_description = models.CharField('Описание сайта', max_length=1000,
                                        default='Лучший сервис доставки правильного питания.<br>Ешь вкусно. Худей легко!')
    open_graph_site_name = models.CharField('Open Graph site_name', max_length=200, default='')
    open_graph_title = models.CharField('Open Graph title', max_length=200, default='')
    open_graph_description = models.CharField('Open Graph description', max_length=1000, default='')
    open_graph_image = models.ImageField('Open Graph image', upload_to='global/',
                                         help_text='1200x627px, основное содержимое (текст) в центре', null=True,
                                         blank=True)
    separator = models.CharField('Разделитель Title',
                                 help_text='Google.com | Поиск (Тут "|")',
                                 max_length=10, default='|')
    base = models.CharField('Домен сайта', help_text='Например: google.com', max_length=100)
    phone_number = models.CharField('Контактный номер телефона', max_length=20)
    whatsapp_number = models.PositiveBigIntegerField('WhatsApp номер',
                                                     help_text='В междунарожном формате, подробнее <a href="https://faq.whatsapp.com/general/chats/how-to-use-click-to-chat" target="_blank">тут</a>')
    instagram_username = models.CharField('Instagram username', max_length=50)
    facebook_username = models.CharField('Facebook username', help_text='https://facebook.com/<ваш username>/',
                                         max_length=50)
    notification_mails = models.TextField('Email-ы для оповещений через Enter', blank=True, null=True)
    green_api_id_instance = models.PositiveSmallIntegerField('Green API Instance ID',
                                                             help_text='ЛК Green API -> Сверху "Инстантс аккаунта Whatsapp" - "Whatsapp #(Это число)"',
                                                             default=8771, blank=True, null=True)
    green_api_api_token_instance = models.CharField('Green API Instance Token',
                                                    help_text='ЛК Green API -> "Токен Api: (Эта строка)"',
                                                    default='f0aae8ed17bb0218cc614361535f5e12994b1bc3ba664e14bc',
                                                    max_length=500, blank=True, null=True)
    notification_phones = models.TextField('Номера телефонов Whatsapp для оповещений через Enter', blank=True,
                                           null=True)
    promocode_sale = models.IntegerField('Скидка с промокода', default=20)
    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Пресет настройки'
        verbose_name_plural = 'Глобальные настройки'

    def save(self, *args, **kwargs):
        if self.active:
            Fixed.objects.filter(active=self.active).update(active=False)
        if self.promocode_sale <= 0:
            self.promocode_sale = 1
        if self.promocode_sale >= 100:
            self.promocode_sale = 99
        super(Fixed, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активный пресет настроек'
        else:
            return 'Пресет настроек %s' % self.id


@receiver(pre_save, sender=Fixed)
def fixed_pre_save(sender, instance, **kwargs):
    add_webp_image(instance.logo, instance.logo_webp)


@receiver(post_save, sender=Fixed)
def generate_icons(sender, instance, **kwargs):
    # Генерация иконок
    formats = [180, 167, 152, 144, 120, 114, 76, 57]
    icon_root_path = os.path.join(settings.MEDIA_ROOT, 'icons')
    for form in formats:
        img = Image.open(instance.icon.path)
        img.thumbnail((form, form))
        img.save(os.path.join(icon_root_path, f'apple-touch-icon-{form}x{form}.png'), 'PNG')
    img = Image.open(instance.icon.path)
    img.thumbnail((57, 57))
    img.save(os.path.join(icon_root_path, 'apple-touch-icon.png'), 'PNG')
    img = Image.open(instance.icon.path)
    img.thumbnail((120, 120))
    img.save(os.path.join(icon_root_path, 'favicon.ico'), 'ICO')
    img = Image.open(instance.icon.path)
    img.thumbnail((50, 50))
    img.save(instance.icon.path)


@receiver(post_save, sender=Fixed)
def convert_logo(sender, instance, **kwargs):
    if instance.logo:
        img = Image.open(instance.logo.path)
        img.save(instance.logo.path + '.png', 'PNG')


class Video(models.Model):
    video_ru_mp4 = models.FileField('Русский mp4', upload_to='global/videos/ru/', blank=True, null=True)
    video_ru_webm = models.FileField('Русский webm', upload_to='global/videos/ru/', blank=True, null=True)
    video_ru_ogg = models.FileField('Русский ogg', upload_to='global/videos/ru/', blank=True, null=True)
    video_he_mp4 = models.FileField('Иврит mp4', upload_to='global/videos/he/', blank=True, null=True)
    video_he_webm = models.FileField('Иврит webm', upload_to='global/videos/he/', blank=True, null=True)
    video_he_ogg = models.FileField('Иврит ogg', upload_to='global/videos/he/', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        if self.active:
            return 'Активный пресет видео'
        else:
            return 'Пресет видео %s' % self.id


class WrapperTranslations(models.Model):
    """ Перевод статичных данных """
    logout = models.CharField('Выйти', default='Выйти', max_length=200)
    login = models.CharField('Войти', default='Войти', max_length=200)
    logging_in = models.CharField('Вход', default='Вход', max_length=200)
    user_login = models.CharField('Email или номер телефона', default='Email или номер телефона', max_length=200)
    password = models.CharField('Пароль', default='Пароль', max_length=200)
    remember_me = models.CharField('Запомнить меня', default='Запомнить меня', max_length=200)
    forget_password = models.CharField('Забыли пароль?', default='Забыли пароль?', max_length=200)
    registration = models.CharField('Регистрация', default='Регистрация', max_length=200)
    user_name = models.CharField('Имя', default='Имя', max_length=200)
    user_surname = models.CharField('Фамилия', default='Фамилия', max_length=200)
    user_phone = models.CharField('Телефон', default='Телефон', max_length=200)
    signup_by_email = models.CharField('или email', default='или email', max_length=200)
    signup_by_phone = models.CharField('или телефон', default='или телефон', max_length=200)
    error_phone_russia = models.CharField('На данный момент принимаются только российские операторы.',
                                          default='На данный момент принимаются только российские операторы.',
                                          max_length=200)
    error_phone_short = models.CharField('Заполните номер полностью.', default='Заполните номер полностью.',
                                         max_length=200)
    next = models.CharField('Далее', default='Далее', max_length=200)
    error_email_exists = models.CharField('Такой email уже есть в системе.', default='Такой email уже есть в системе.',
                                          max_length=200)
    error_phone_exists = models.CharField('Такой телефон уже есть в системе.',
                                          default='Такой телефон уже есть в системе.', max_length=200)
    error_no_register_data = models.CharField('Обязательное поле.', default='Обязательное поле.', max_length=200)
    user_sex = models.CharField('Пол', default='Пол', max_length=200)
    repeat_password = models.CharField('Повторите пароль', default='Повторите пароль', max_length=200)
    agreed = models.CharField('Я принимаю $1правила сервиса$2', default='Я принимаю $1правила сервиса$2',
                              help_text='Оставить $1 и $2!!!', max_length=200)
    reset_password = models.CharField('Сбросить пароль', default='Сбросить пароль', max_length=200)
    user_agreement = models.CharField('Пользовательское соглашение', default='Пользовательское соглашение', max_length=200)
    privacy_policy = models.CharField('Политика конфеденциальности', default='Политика конфеденциальности', max_length=200)
    language = models.CharField('Язык', default='Язык', max_length=200)
    email_confirmed = models.CharField('Email подтвержден!', default='Email подтвержден!', max_length=200)
    please_login = models.CharField('Войдите в систему.', default='Войдите в систему.', max_length=200)
    success = models.CharField('Успешно!', default='Успешно!', max_length=200)
    wait_a_second = models.CharField('Подождите секундочку...', default='Подождите секундочку...', max_length=200)
    error = models.CharField('Ошибка!', default='Ошибка!', max_length=200)
    try_again = models.CharField('Введите правильные данные.',
                                 default='Введите правильные данные.', max_length=200)
    confirm_instruction = models.CharField('Для продолжения перейдите по ссылке, отправленной на ваш email.',
                                           default='Для продолжения перейдите по ссылке, отправленной на ваш email.',
                                           max_length=200)
    agreed_error = models.CharField('Для регистрации нужно принять правила сервиса.',
                                    default='Для регистрации нужно принять правила сервиса.', max_length=200)
    no_such_email = models.CharField('Такого email-a нет в системе.', default='Такого email-a нет в системе.',
                                     max_length=200)
    bad_key = models.CharField('Неправильный ключ!', default='Неправильный ключ!', max_length=200)
    key_resented = models.CharField('Ключ успешно отправлен!', default='Ключ успешно отправлен!', max_length=200)
    key_info = models.CharField('Введите, код отправленный на указанные данные',
                                default='Введите, код отправленный на указанные данные', max_length=200)
    resend_key = models.CharField('Повторить отправку', default='Повторить отправку', max_length=200)
    personal_account = models.CharField('Личный кабинет', default='Личный кабинет', max_length=200)
    wrong_password = models.CharField('Неверный пароль.', default='Неверный пароль.', max_length=200)
    user_address = models.CharField('Адрес доставки', default='Адрес доставки', max_length=200)
    why_us = models.CharField('Почему мы', default='Почему мы', max_length=200)
    our_menu = models.CharField('Наше меню', default='Наше меню', max_length=200)
    reviews = models.CharField('Отзывы', default='Отзывы', max_length=200)
    questions = models.CharField('Вопросы', default='Вопросы', max_length=200)
    call = models.CharField('Позвонить', default='Позвонить', max_length=200)
    call_me = models.CharField('Перезвоните мне', default='Перезвоните мне', max_length=200)
    form_fail_info = models.CharField('Проверьте введенные данные. Исключите из текста символы "<" ">".',
                                      default='Проверьте введенные данные. Исключите из текста символы "<" ">".',
                                      max_length=200)
    call_me_success_info = models.CharField('Ваша заявка принята! Мы перезвоним вам в ближайшее время.',
                                            default='Ваша заявка принята! Мы перезвоним вам в ближайшее время.',
                                            max_length=200)
    name_and_surname = models.CharField('Имя и фамилия', default='Имя и фамилия', max_length=200)
    send = models.CharField('Отправить', default='Отправить', max_length=200)

    order_created = models.CharField('Заказ создан', default='Заказ создан', max_length=200)
    order_success = models.CharField('Ваш заказ успешно создан!', default='Ваш заказ успешно создан!', max_length=200)
    unique_order_number = models.CharField('Уникальный номер заказа', default='Уникальный номер заказа', max_length=200)
    to_pay = models.CharField('К оплате', default='К оплате', max_length=200)
    order_success_info = models.CharField(
        'В ближайшее время с вами свяжется наш оператор для уточнения деталей доставки.',
        default='В ближайшее время с вами свяжется наш оператор для уточнения деталей доставки.', max_length=200)
    order_not_created = models.CharField('Заказ не создан', default='Заказ не создан', max_length=200)
    code = models.CharField('Код', default='Код', max_length=200)
    email = models.CharField('Email', default='Email', max_length=200)
    footer_info1 = models.CharField(
        'Фотографии блюд являются вариантом сервировки блюда. Внешний вид блюда может отличаться от фотографий на сайте',
        default='Фотографии блюд являются вариантом сервировки блюда. Внешний вид блюда может отличаться от фотографий на сайте',
        max_length=500)
    footer_info2 = models.CharField(
        'Указывая номер телефона или e-mail на сайте, Вы соглашаетесь с условиями публичной оферты и обработки персональных данных',
        default='Указывая номер телефона или e-mail на сайте, Вы соглашаетесь с условиями публичной оферты и обработки персональных данных',
        max_length=500)
    info_video = models.CharField('Инструкция к сайту', default='Инструкция к сайту', max_length=200)
    phone_10_error = models.CharField('Минимум 10 символов. Пример: +972001112222',
                                      default='Минимум 10 символов. Пример: +972001112222', max_length=200)
    calories_short_start = models.CharField('от', default='от', max_length=200)
    calories_short = models.CharField('Ккал', default='Ккал', max_length=200)
    payment_type = models.CharField('Метод оплаты', default='Метод оплаты', max_length=200)
    card_phone = models.CharField('Картой по телефону', default='Картой по телефону', max_length=200)
    card_delivery = models.CharField('Картой курьеру', default='Картой курьеру', max_length=200)
    cash_delivery = models.CharField('Наличными курьеру', default='Наличными курьеру', max_length=200)

    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Пресет перевода'
        verbose_name_plural = 'Перевод'

    def save(self, *args, **kwargs):
        if self.active:
            WrapperTranslations.objects.filter(active=self.active).update(active=False)
        super(WrapperTranslations, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активный пресет перевода'
        else:
            return 'Пресет перевода %s' % str(self.id)


class PrivacyPolicy(models.Model):
    content = RichTextField('Политика конфеденциальности', null=True, blank=True)
    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Политика конфеденциальностии'
        verbose_name_plural = 'Политика конфеденциальности'

    def save(self, *args, **kwargs):
        if self.active:
            PrivacyPolicy.objects.filter(active=self.active).update(active=False)
        super(PrivacyPolicy, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активная политика конфеденциальности'
        else:
            return 'Пресет политики конфеденциальности %s' % self.id


class UserAgreement(models.Model):
    content = RichTextField('Пользовательское соглашение', null=True, blank=True)
    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Пользовательское соглашение'
        verbose_name_plural = 'Пользовательские соглашения'

    def save(self, *args, **kwargs):
        if self.active:
            UserAgreement.objects.filter(active=self.active).update(active=False)
        super(UserAgreement, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активное пользовательское соглашение'
        else:
            return 'Пресет Пользовательскиого соглашения %s' % self.id


class Dish(models.Model):
    """ Блюда """
    admin_name = models.CharField('Название для админа', max_length=120)
    name = models.CharField('Название', max_length=120)
    type = models.CharField('Тип', choices=(
        ('breakfast', 'Завтрак'),
        ('second-breakfast', 'Второй завтрак'),
        ('lunch', 'Обед'),
        ('high-tea', 'Полдник'),
        ('dinner', 'Ужин'),
        ('drink', 'Напиток')
    ), max_length=50)
    image = models.ImageField('Изображение', help_text='Рекомендуемо 720x530, формат webp', upload_to='dishes/')
    image_webp = models.ImageField('Изображение webp', help_text='Рекомендуемо 720x530, формат webp', upload_to='',
                                   editable=False, blank=True, null=True)
    description = models.CharField('Описание', max_length=500)
    calories = models.IntegerField('Калории (в мужской версии)')
    weight = models.IntegerField('Вес в граммах (в мужской версии)')
    proteins = models.IntegerField('Белки (в мужской версии)')
    fats = models.IntegerField('Жиры (в мужской версии)')
    carbohydrates = models.IntegerField('Углеводы (в мужской версии)')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['admin_name']

    def __str__(self):
        return self.admin_name


@receiver(pre_save, sender=Dish)
def dish_pre_save(sender, instance, **kwargs):
    add_webp_image(instance.image, instance.image_webp)


@receiver(post_save, sender=Dish)
def compress_images(sender, instance, **kwargs):
    if instance.image:
        img = Image.open(instance.image.path)
        img.thumbnail((720, 530))
        img.save(instance.icon.path + '.png', 'PNG')


class MenuType(models.Model):
    name = models.CharField('Полное название', max_length=50)
    short_description = models.CharField('Короткое описание', default='Полезно для мышц', max_length=30)
    extra_short_description = models.CharField('Окень короткое описание', default='от 10$/мес', max_length=20)
    description = models.CharField('Описание', max_length=300)
    image = models.ImageField('Фоновое изображение плана', help_text='Рекомендуемо 920x1000, формат webp',
                              upload_to='menu-types/', null=True, blank=True)
    image_webp = models.ImageField('Фоновое изображение плана webp',
                                   help_text='Рекомендуемо 920x1000, формат webp',
                                   upload_to='', null=True, blank=True, editable=False)
    order = models.PositiveSmallIntegerField('Порядковый номер', default=1)
    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def save(self, *args, **kwargs):
        if MenuType.objects.filter(order=self.order).exclude(id=self.id):
            self.order = MenuType.objects.all().aggregate(Max('order'))['order__max'].order + 1
        super(MenuType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=MenuType)
def menu_type_pre_save(sender, instance, **kwargs):
    if instance.image:
        add_webp_image(instance.image, instance.image_webp)


class Menu(models.Model):
    """ Меню """
    type = models.ForeignKey(MenuType, verbose_name='Тип меню', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Название', max_length=50)
    description = models.CharField('Описание', max_length=300)
    calories = models.IntegerField('Калорий', default=2000)
    day1 = models.ManyToManyField(Dish, verbose_name='Первый 1 стандартно', related_name='day1', blank=True,
                                  null=True)
    day1_other = models.ManyToManyField(Dish, verbose_name='Первый 1 все блюда', related_name='day1_other',
                                        blank=True, null=True)
    day2 = models.ManyToManyField(Dish, verbose_name='Второй день стандартно', related_name='day2', blank=True,
                                  null=True)
    day2_other = models.ManyToManyField(Dish, verbose_name='Второй день все блюда', related_name='day2_other',
                                        blank=True, null=True)
    day3 = models.ManyToManyField(Dish, verbose_name='Третий день стандартно', related_name='day3', blank=True,
                                  null=True)
    day3_other = models.ManyToManyField(Dish, verbose_name='Третий день все блюда', related_name='day3_other',
                                        blank=True, null=True)
    day4 = models.ManyToManyField(Dish, verbose_name='Четвертый день стандартно', related_name='day4', blank=True,
                                  null=True)
    day4_other = models.ManyToManyField(Dish, verbose_name='Четвертый день все блюда', related_name='day4_other',
                                        blank=True, null=True)
    day5 = models.ManyToManyField(Dish, verbose_name='Пятный день стандартно', related_name='day5', blank=True,
                                  null=True)
    day5_other = models.ManyToManyField(Dish, verbose_name='Пятный день все блюда', related_name='day5_other',
                                        blank=True, null=True)
    day6 = models.ManyToManyField(Dish, verbose_name='Шестой день стандартно', related_name='day6', blank=True,
                                  null=True)
    day6_other = models.ManyToManyField(Dish, verbose_name='Шестой день все блюда', related_name='day6_other',
                                        blank=True, null=True)
    day7 = models.ManyToManyField(Dish, verbose_name='Седьмой день стандартно', related_name='day7',
                                  blank=True,
                                  null=True)
    day7_other = models.ManyToManyField(Dish, verbose_name='Седьмой день все блюда',
                                        related_name='day7_other',
                                        blank=True, null=True)
    day8 = models.ManyToManyField(Dish, verbose_name='Восьмой день стандартно', related_name='day8',
                                  blank=True,
                                  null=True)
    day8_other = models.ManyToManyField(Dish, verbose_name='Восьмой день все блюда',
                                        related_name='day8_other',
                                        blank=True, null=True)
    day9 = models.ManyToManyField(Dish, verbose_name='Девятый день стандартно', related_name='day9',
                                  blank=True,
                                  null=True)
    day9_other = models.ManyToManyField(Dish, verbose_name='Девятый день все блюда',
                                        related_name='day9_other',
                                        blank=True, null=True)
    day10 = models.ManyToManyField(Dish, verbose_name='Десятый день стандартно', related_name='day10',
                                   blank=True,
                                   null=True)
    day10_other = models.ManyToManyField(Dish, verbose_name='Десятый день все блюда',
                                         related_name='day10_other',
                                         blank=True, null=True)
    day11 = models.ManyToManyField(Dish, verbose_name='Одиннадцатый день стандартно', related_name='day11',
                                   blank=True,
                                   null=True)
    day11_other = models.ManyToManyField(Dish, verbose_name='Одиннадцатый день все блюда',
                                         related_name='day11_other',
                                         blank=True, null=True)
    day12 = models.ManyToManyField(Dish, verbose_name='Двенадцатый день стандартно', related_name='day12',
                                   blank=True,
                                   null=True)
    day12_other = models.ManyToManyField(Dish, verbose_name='Двенадцатый день все блюда',
                                         related_name='day12_other',
                                         blank=True, null=True)
    day13 = models.ManyToManyField(Dish, verbose_name='Тринадцатый день стандартно', related_name='day13',
                                   blank=True,
                                   null=True)
    day13_other = models.ManyToManyField(Dish, verbose_name='Тринадцатый день все блюда',
                                         related_name='day13_other',
                                         blank=True, null=True)
    day14 = models.ManyToManyField(Dish, verbose_name='Четырнадцатый день стандартно', related_name='day14',
                                   blank=True,
                                   null=True)
    day14_other = models.ManyToManyField(Dish, verbose_name='Четырнадцатый день все блюда',
                                         related_name='day14_other',
                                         blank=True, null=True)
    day15 = models.ManyToManyField(Dish, verbose_name='Пятнадцатый день стандартно', related_name='day15',
                                   blank=True,
                                   null=True)
    day15_other = models.ManyToManyField(Dish, verbose_name='Пятнадцатый день все блюда',
                                         related_name='day15_other',
                                         blank=True, null=True)
    day16 = models.ManyToManyField(Dish, verbose_name='Шестнадцатый день стандартно', related_name='day16',
                                   blank=True,
                                   null=True)
    day16_other = models.ManyToManyField(Dish, verbose_name='Шестнадцатый день все блюда',
                                         related_name='day16_other',
                                         blank=True, null=True)
    day17 = models.ManyToManyField(Dish, verbose_name='Семнадцатый день стандартно', related_name='day17',
                                   blank=True,
                                   null=True)
    day17_other = models.ManyToManyField(Dish, verbose_name='Семнадцатый день все блюда',
                                         related_name='day17_other',
                                         blank=True, null=True)
    day18 = models.ManyToManyField(Dish, verbose_name='Восемнадцатый день стандартно', related_name='day18',
                                   blank=True,
                                   null=True)
    day18_other = models.ManyToManyField(Dish, verbose_name='Восемнадцатый день все блюда',
                                         related_name='day18_other',
                                         blank=True, null=True)
    day19 = models.ManyToManyField(Dish, verbose_name='Девятнадцатый день стандартно', related_name='day19',
                                   blank=True,
                                   null=True)
    day19_other = models.ManyToManyField(Dish, verbose_name='Девятнадцатый день все блюда',
                                         related_name='day19_other',
                                         blank=True, null=True)
    day20 = models.ManyToManyField(Dish, verbose_name='Двадцатый день стандартно', related_name='day20',
                                   blank=True,
                                   null=True)
    day20_other = models.ManyToManyField(Dish, verbose_name='Двадцатый день все блюда',
                                         related_name='day20_other',
                                         blank=True, null=True)
    day21 = models.ManyToManyField(Dish, verbose_name='Двадцать первый день стандартно', related_name='day21',
                                   blank=True,
                                   null=True)
    day21_other = models.ManyToManyField(Dish, verbose_name='Двадцать первый день все блюда',
                                         related_name='day21_other',
                                         blank=True, null=True)
    day22 = models.ManyToManyField(Dish, verbose_name='Двадцать второй день стандартно', related_name='day22',
                                   blank=True,
                                   null=True)
    day22_other = models.ManyToManyField(Dish, verbose_name='Двадцать второй день все блюда',
                                         related_name='day22_other',
                                         blank=True, null=True)
    day23 = models.ManyToManyField(Dish, verbose_name='Двадцать третий день стандартно', related_name='day23',
                                   blank=True,
                                   null=True)
    day23_other = models.ManyToManyField(Dish, verbose_name='Двадцать третий день все блюда',
                                         related_name='day23_other',
                                         blank=True, null=True)
    day24 = models.ManyToManyField(Dish, verbose_name='Двадцать четвертый день стандартно', related_name='day24',
                                   blank=True,
                                   null=True)
    day24_other = models.ManyToManyField(Dish, verbose_name='Двадцать четвертый день все блюда',
                                         related_name='day24_other',
                                         blank=True, null=True)
    day25 = models.ManyToManyField(Dish, verbose_name='Двадцать пятый день стандартно', related_name='day25',
                                   blank=True,
                                   null=True)
    day25_other = models.ManyToManyField(Dish, verbose_name='Двадцать пятый день все блюда',
                                         related_name='day25_other',
                                         blank=True, null=True)
    day26 = models.ManyToManyField(Dish, verbose_name='Двадцать шестой день стандартно', related_name='day26',
                                   blank=True,
                                   null=True)
    day26_other = models.ManyToManyField(Dish, verbose_name='Двадцать шестой день все блюда',
                                         related_name='day26_other',
                                         blank=True, null=True)
    days1_price = models.DecimalField('1 день цена', decimal_places=2, max_digits=8,
                                     default=10)
    days2_price = models.DecimalField('2 дня цена', decimal_places=2, max_digits=8,
                                     default=10)
    days4_price = models.DecimalField('4 дня цена', decimal_places=2, max_digits=8,
                                     default=10)
    days6_price = models.DecimalField('6 дней цена', decimal_places=2, max_digits=8,
                                     default=10)
    days14_price = models.DecimalField('14 дней цена', decimal_places=2, max_digits=8,
                                     default=10)
    days26_price = models.DecimalField('26 дней цена', decimal_places=2, max_digits=8,
                                     default=10)
    home_order = models.PositiveSmallIntegerField('Порядковый номер', default=1)

    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def save(self, *args, **kwargs):
        if Menu.objects.filter(type=self.type, order=self.home_order).exclude(id=self.id):
            self.home_order = Menu.objects.filter(type=self.type).aggregate(Max('home_order'))['home_order__max'].home_order + 1
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return f'Меню {self.type} - {self.name} - {self.calories} ккал - {"Активно" if self.active else "Неактвино"}'


class HomePageSettings(models.Model):
    """ Настройки главной """
    title = models.CharField('Заголовок страницы (Meta Title)', help_text='Используется в SEO', max_length=200)
    meta_description = models.TextField('Meta Description', help_text='Используется в SEO', null=True, blank=True)
    meta_keywords = models.TextField('Meta Keywords', help_text='Используется в SEO', null=True, blank=True)
    open_graph_title = models.CharField('Open Graph title', help_text='Используется в SEO', max_length=200, null=True,
                                        blank=True)
    open_graph_description = models.CharField('Open Graph description', help_text='Используется в SEO', max_length=200,
                                              null=True, blank=True)
    open_graph_image = models.ImageField('Open Graph image', help_text='Используется в SEO', upload_to='homepage/',
                                         null=True, blank=True)
    slider_title = models.CharField('Большой текст на слайдере', max_length=40, null=True, blank=True)
    slider_description = RichTextField('Небольшое описание на слайдере', max_length=1000, null=True, blank=True)
    slider_overlay = models.IntegerField('Затемнение слайдера', help_text='0-99', default='75')
    slider_image_1 = models.ImageField('Изображение для главного слайдера №1',
                                       help_text='Рекомендуемо 4096x3072, формат webp',
                                       upload_to='homepage/slider/', null=True, blank=True)
    slider_image_1_webp = models.ImageField('Изображение для главного слайдера №1 webp',
                                            help_text='Рекомендуемо 4096x3072, формат webp',
                                            upload_to='', null=True, blank=True, editable=False)
    slider_image_2 = models.ImageField('Изображение для главного слайдера №2',
                                       help_text='Рекомендуемо 4096x3072, формат webp',
                                       upload_to='homepage/slider/', null=True, blank=True)
    slider_image_2_webp = models.ImageField('Изображение для главного слайдера №2 webp',
                                            help_text='Рекомендуемо 4096x3072, формат webp',
                                            upload_to='', null=True, blank=True, editable=False)
    slider_image_3 = models.ImageField('Изображение для главного слайдера №3',
                                       help_text='Рекомендуемо 4096x3072, формат webp',
                                       upload_to='homepage/slider/', null=True, blank=True)
    slider_image_3_webp = models.ImageField('Изображение для главного слайдера №2 webp',
                                            help_text='Рекомендуемо 4096x3072, формат webp',
                                            upload_to='', null=True, blank=True, editable=False)
    slider_image_4 = models.ImageField('Изображение для главного слайдера №3',
                                       help_text='Рекомендуемо 4096x3072, формат webp',
                                       upload_to='homepage/slider/', null=True, blank=True)
    slider_image_4_webp = models.ImageField('Изображение для главного слайдера №4 webp',
                                            help_text='Рекомендуемо 4096x3072, формат webp',
                                            upload_to='', null=True, blank=True, editable=False)
    slider_image_5 = models.ImageField('Изображение для главного слайдера №5',
                                       help_text='Рекомендуемо 4096x3072, формат webp',
                                       upload_to='homepage/slider/', null=True, blank=True)
    slider_image_5_webp = models.ImageField('Изображение для главного слайдера №5 webp',
                                            help_text='Рекомендуемо 4096x3072, формат webp',
                                            upload_to='', null=True, blank=True, editable=False)
    pluses1_title = models.CharField('Название преимущества №1', max_length=50, default='Не надо готовки')
    pluses1_description = models.CharField('Описание преимущества №1', max_length=200,
                                           default='С нашим сервисом вы сэкономите кучу времени на походах в магазин '
                                                   'и приготовлении пищи. Больше не надо готовить!')
    pluses1_icon = models.CharField('Иконка первого преимущества (класс fontawesome 5)', max_length=40,
                                    default='fas fa-clock')
    pluses2_title = models.CharField('Название преимущества №2', max_length=50, default='Оставайтесь в форме')
    pluses2_description = models.CharField('Описание преимущества №2', max_length=200,
                                           default='Если вы всегда мечтали вкусно питаться и оставаться в форме - это '
                                                   'лучший вариант для вас. Выберите план питания и наслаждайтесь '
                                                   'жизнью, не ограничивая себя!')
    pluses2_icon = models.CharField('Иконка второго преимущества (класс fontawesome 5)', max_length=40,
                                    default='fas fa-weight')
    pluses3_title = models.CharField('Название преимущества №3', max_length=50, default='Правильное питание')
    pluses3_description = models.CharField('Описание преимущества №3', max_length=200,
                                           default='Наша продукция изготавлевается из натуральных материалов и имеет '
                                                   'оптимальные для вас параметры. Забудьте о проблемах с '
                                                   'пищеварением!')
    pluses3_icon = models.CharField('Иконка третьего преимущества (класс fontawesome 5)', max_length=40,
                                    default='fas fa-heartbeat')
    new_order = models.CharField('Новый заказ', default='Новый заказ', max_length=200)
    call_us = models.CharField('Позвонить нам', default='Позвонить нам', max_length=200)
    select_menu = models.CharField('Выбрать меню', default='Выбрать меню', max_length=200)
    select_your_aim = models.CharField('Выбери свою цель', default='Выбери свою цель', max_length=200)
    select = models.CharField('Выбрать', default='Выбрать', max_length=200)
    selected = models.CharField('Выбрано', default='Выбрано', max_length=200)
    monday_short = models.CharField('Пн', default='Пн', help_text='Сокращенное название дня недели', max_length=200)
    tuesday_short = models.CharField('Вт', default='Вт', help_text='Сокращенное название дня недели', max_length=200)
    wednesday_short = models.CharField('Ср', default='Ср', help_text='Сокращенное название дня недели', max_length=200)
    thursday_short = models.CharField('Чт', default='Чт', help_text='Сокращенное название дня недели', max_length=200)
    friday_short = models.CharField('Пт', default='Пт', help_text='Сокращенное название дня недели', max_length=200)
    saturday_short = models.CharField('Сб', default='Сб', help_text='Сокращенное название дня недели', max_length=200)
    sunday_short = models.CharField('Вс', default='Вс', help_text='Сокращенное название дня недели', max_length=200)
    want_this_menu = models.CharField('Хочу это меню', default='Хочу это меню', max_length=200)
    order = models.CharField('Заказать', default='Заказать', max_length=200)
    meal_days_1 = models.CharField('1 день питания', default='1 день питания', max_length=200)
    meal_days_2 = models.CharField('2 дня питания', default='2 дня питания', max_length=200)
    meal_days_4 = models.CharField('4 дня питания', default='4 дня питания', max_length=200)
    meal_days_6 = models.CharField('6 дней питания', default='6 дней питания', max_length=200)
    meal_days_14 = models.CharField('14 дней питания', default='14 дней питания', max_length=200)
    meal_days_26 = models.CharField('26 дней питания', default='26 дней питания', max_length=200)
    your_profit = models.CharField('Ваша выгода', default='Ваша выгода', max_length=200)
    phone_info = models.CharField('Для уточнения деталей заказа и доставки',
                                  default='Для уточнения деталей заказа и доставки', max_length=200)
    comment = models.CharField('Комментарий', default='Комментарий', max_length=200)
    show_all = models.CharField('Показать все', default='Показать все', max_length=200)
    write_review = models.CharField('Оставить отзыв', default='Оставить отзыв', max_length=200)
    often_questions = models.CharField('Частые вопросы', default='Частые вопросы', max_length=200)
    review = models.CharField('Отзыв', default='Отзыв', max_length=200)
    contact_link = models.CharField('Контактная ссылка', default='Контактная ссылка', max_length=200)
    contact_link_info = models.CharField('Пожалуйста укажите ссылку на любой из ваших аккаунтов в социальных сетях.',
                                         default='Пожалуйста укажите ссылку на любой из ваших аккаунтов в социальных сетях.',
                                         max_length=200)
    select_dish = models.CharField('Выбрать блюдо', default='Выбрать блюдо', max_length=200)
    back = models.CharField('Назад', default='Назад', max_length=200)
    write_review_success_info = models.CharField(
        'Вы успешно отправили отзыв. После модерации он будет добавлен в блок.',
        default='Вы успешно отправили отзыв. После модерации он будет добавлен в блок.', max_length=200)
    drink = models.CharField('Напиток', default='Напиток', max_length=200)
    breakfast = models.CharField('Завтрак', default='Завтрак', max_length=200)
    second_breakfast = models.CharField('Второй завтрак', default='Второй завтрак', max_length=200)
    lunch = models.CharField('Обед', default='Обед', max_length=200)
    high_tea = models.CharField('Полдник', default='Полдник', max_length=200)
    dinner = models.CharField('Ужин', default='Ужин', max_length=200)
    replace = models.CharField('Заменить', default='Заменить', max_length=200)
    gram_short = models.CharField('г', default='г', help_text='Сокращение грамм', max_length=200)
    summary = models.CharField('Всего', default='Всего', max_length=200)
    proteins = models.CharField('Белки', default='Белки', max_length=200)
    fats = models.CharField('Жиры', default='Жиры', max_length=200)
    carbohydrates = models.CharField('Углеводы', default='Углеводы', max_length=200)
    to_price = models.CharField('к цене', default='к цене', max_length=200)
    from_price = models.CharField('от цены', default='от цены', max_length=200)
    changed_dishes = models.CharField('Измененные блюда', default='Измененные блюда', max_length=200)
    reset = models.CharField('Сбросить', default='Сбросить', max_length=200)
    per_day = models.CharField('за день', default='за день', max_length=200)
    all_days = models.CharField('за заказ', default='за заказ', max_length=200)
    order_failure = models.CharField('На сервере произошли изменения во время создания заказа',
                                     default='На сервере произошли изменения во время создания заказа', max_length=200)
    order_failure_info_1 = models.CharField(
        'Наш сервис никогда не обманывает своих покупателей, потому заказ не был создан',
        default='Наш сервис никогда не обманывает своих покупателей, потому заказ не был создан', max_length=200)
    order_failure_info_2 = models.CharField('Пожалуйста обновите страницу и введите данные снова',
                                            default='Пожалуйста обновите страницу и введите данные снова',
                                            max_length=200)
    reload_page = models.CharField('Обновить страницу', default='Обновить страницу', max_length=200)

    delivery_map = models.ImageField('Карта доставки',
                                     help_text='Рекомендуемо 800x600, формат webp',
                                     upload_to='homepage/maps/',
                                     null=True, blank=True)
    delivery_map_webp = models.ImageField('Карта доставки webp',
                                          help_text='Рекомендуемо 800x600, формат webp',
                                          upload_to='',
                                          null=True, blank=True, editable=False)
    free_delivery = models.CharField('Бесплатная доставка', default='Бесплатная доставка', max_length=200)
    free_delivery_text_1 = models.CharField('Доставим еду по Израилю бесплатно!',
                                            default='Доставим еду по Израилю бесплатно!', max_length=200)
    free_delivery_text_2 = models.CharField('Бесплатная доставка в выделенной области',
                                            default='Бесплатная доставка в выделенной области', max_length=200)
    select_plan1 = models.CharField('Выберите тип питания для взаимодействия с меню',
                                            default='Выберите тип питания для взаимодействия с меню',
                                            max_length=200)
    select_plan2 = models.CharField('Выберите план питания',
                                    default='Выберите план питания', max_length=200)
    select_days = models.CharField('Выберите количество дней', default='Выберите количество дней', max_length=200)
    calculate_calories = models.CharField('Расчитать калории', default='Расчитать калории', max_length=200)
    calories_calculator = models.CharField('Калькулятор калорий', default='Калькулятор калорий', max_length=200)
    age = models.CharField('Возраст', default='Возраст', max_length=200)
    height = models.CharField('Рост', default='Рост', max_length=200)
    weight = models.CharField('Вес', default='Вес', max_length=200)
    sex = models.CharField('Пол', default='Пол', max_length=200)
    male = models.CharField('Мужской', default='Мужской', max_length=200)
    female = models.CharField('Женский', default='Женский', max_length=200)
    physical_activities = models.CharField('Физическая активность', default='Физическая активность', max_length=200)
    physical_activities1 = models.CharField('Нет физической активности', default='Нет физической активности', max_length=200)
    physical_activities2 = models.CharField('2-3 раза в неделю неинтенсивных тренировок', default='2-3 раза в неделю неинтенсивных тренировок', max_length=200)
    physical_activities3 = models.CharField('Постоянные интенсивные тренировки', default='Постоянные интенсивные тренировки', max_length=200)
    purpose = models.CharField('Цель', default='Цель', max_length=200)
    purpose1 = models.CharField('Поддерживать вес', default='Поддерживать вес', max_length=200)
    purpose2 = models.CharField('Сбросить вес', default='Сбросить вес', max_length=200)
    purpose3 = models.CharField('Набрать массу', default='Набрать массу', max_length=200)
    you_need_calories = models.CharField('Ваша дневная норма калорий:', default='Ваша дневная норма калорий:', max_length=200)
    recommended_menus = models.CharField('Рекомендованые меню', default='Рекомендованые меню', max_length=200)
    result = models.CharField('Результат', default='Результат', max_length=200)
    promocode = models.CharField('Введите промокод, если есть', default='Введите промокод, если есть', max_length=200)

    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Пресет настройки главной'
        verbose_name_plural = 'Настройки главной'

    def save(self, *args, **kwargs):
        if self.active:
            HomePageSettings.objects.filter(active=self.active).update(active=False)
        super(HomePageSettings, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активный пресет настроек'
        else:
            return 'Пресет настроек %s' % self.id


@receiver(pre_save, sender=HomePageSettings)
def home_page_settings_pre_save(sender, instance, **kwargs):
    if instance.slider_image_1:
        add_webp_image(instance.slider_image_1, instance.slider_image_1_webp)
    if instance.slider_image_2:
        add_webp_image(instance.slider_image_2, instance.slider_image_2_webp)
    if instance.slider_image_3:
        add_webp_image(instance.slider_image_3, instance.slider_image_3_webp)
    if instance.slider_image_4:
        add_webp_image(instance.slider_image_4, instance.slider_image_4_webp)
    if instance.slider_image_5:
        add_webp_image(instance.slider_image_5, instance.slider_image_5_webp)
    if instance.delivery_map:
        add_webp_image(instance.delivery_map, instance.delivery_map_webp)


@receiver(post_save, sender=HomePageSettings)
def compress_images(sender, instance, **kwargs):
    for field in [instance.slider_image_1, instance.slider_image_2, instance.slider_image_4, instance.slider_image_4,
                  instance.slider_image_5]:
        if field:
            img = Image.open(field.path)
            img.thumbnail((4096, 3072))
            img.save(field.path + '.png', 'PNG')


class AccountPageSettings(models.Model):
    """ Настройки личного кабинета """
    title = models.CharField('Title', default='Личный кабинет', max_length=200)
    personal_info = models.CharField('Личные данные', default='Личные данные', max_length=200)
    my_profile = models.CharField('Личный кабинет', default='Личный кабинет', max_length=200)
    hello = models.CharField('Добро пожаловать', default='Добро пожаловать', max_length=200)
    save_btn = models.CharField('Сохранить', default='Сохранить', max_length=200)
    changes_saved = models.CharField('Изменения сохранены', default='Изменения сохранены', max_length=200)
    changes_saved_info = models.CharField('Ваши изменения успешно сохранены!',
                                          default='Ваши изменения успешно сохранены!',
                                          max_length=200)
    old_password = models.CharField('Старый пароль', default='Старый пароль', max_length=200)
    change_password = models.CharField('Сменить пароль', default='Сменить пароль', max_length=200)
    new_password = models.CharField('Новый пароль', default='Новый пароль', max_length=200)
    new_password_repeat = models.CharField('Повторите новый пароль', default='Повторите новый пароль', max_length=200)
    change_email = models.CharField('Сменить email', default='Сменить email', max_length=200)
    change_address = models.CharField('Сменить адрес', default='Сменить адрес', max_length=200)
    change_phone = models.CharField('Сменить телефон', default='Сменить телефон', max_length=200)
    add_phone = models.CharField('Добавить телефон', default='Добавить телефон', max_length=200)
    new_phone = models.CharField('Новый телефон', default='Новый телефон', max_length=200)
    add_email = models.CharField('Добавить e-mail', default='Добавить e-mail', max_length=200)
    new_email = models.CharField('Новый email', default='Новый email', max_length=200)
    change_name = models.CharField('Сменить имя', default='Сменить имя', max_length=200)
    change_surname = models.CharField('Сменить фамилию', default='Сменить фамилию', max_length=200)
    change_personal_data = models.CharField('Сменить личные данные', default='Сменить личные данные', max_length=200)
    change_personal_data_success = models.CharField('Личные данные изменены', default='Личные данные изменены',
                                                    max_length=200)
    change_personal_data_info = models.CharField('После проверки администрацией ваши данные будут внесены в систему.',
                                                 default='После проверки администрацией ваши данные будут внесены в '
                                                         'систему.', max_length=200)
    orders = models.CharField('Заказы', default='Заказы', max_length=200)
    load_more = models.CharField('Загрузить ещё', default='Загрузить ещё', max_length=200)
    extend_order = models.CharField('Продлить заказ', default='Продлить заказ', max_length=200)
    days = models.CharField('Дней', default='Дней', max_length=200)
    active_t = models.CharField('Активно', default='Активно', max_length=200)
    completed = models.CharField('Завершено', default='Завершено', max_length=200)
    not_payed = models.CharField('Не оплачено', default='Не оплачено', max_length=200)
    pay = models.CharField('Оплатить онлайн', default='Оплатить онлайн', max_length=200)
    all = models.CharField('Все', default='Все', max_length=200)
    active_pl = models.CharField('Активные', default='Активные', max_length=200)
    completed_pl = models.CharField('Завершенные', default='Завершенные', max_length=200)
    not_payed_pl = models.CharField('Не оплаченные', default='Не оплаченные', max_length=200)
    no_orders = models.CharField('У вас ещё нет заказов', default='У вас ещё нет заказов', max_length=200)
    make_order = models.CharField('Сделать заказ', default='Сделать заказ', max_length=200)
    price = models.CharField('Цена', default='Цена', max_length=200)
    plan_changed = models.CharField('План питания изменился', default='План питания изменился', max_length=200)
    plan_changed_info = models.CharField('Сделайте заказ через форму на главной странице',
                                         default='Сделайте заказ через форму на главной странице', max_length=200)
    home = models.CharField('На главную', default='На главную', max_length=200)
    show_dishes = models.CharField('Показать блюда', default='Показать блюда', max_length=200)
    change_menu = models.CharField('Выбрать другое меню', default='Выбрать другое меню', max_length=200)
    meal_days = models.CharField('Дней питания:', default='Дней питания:', max_length=200)
    you_need_to_pay = models.CharField('Необходимо доплатить:', default='Необходимо доплатить:', max_length=200)
    freeze_info = models.TextField('Информация о заморозке',
                                   default='У вас есть возможность приостановить текущую программу, а после возобновить питание с удобной для вас даты. Заморозка текущего плана приведет к автоматической замене блюд после разморозки.')
    freeze_info_link = models.CharField('Подробнее', default='Подробнее', max_length=200)
    freeze = models.CharField('Заморозить', default='Заморозить', max_length=200)
    unfreeze = models.CharField('Разморозить', default='Разморозить', max_length=200)
    will_be_frozen = models.CharField('Будет заморожено:', default='Будет заморожено:', max_length=200)
    frozen = models.CharField('Заморожено', default='Заморожено', max_length=200)
    will_be_unfrozen = models.CharField('Будет разморожено:', default='Будет разморожено:', max_length=200)
    order_freeze_info = models.CharField('Ваша заявка на заморозку заказа принята, вскоре мы с вами свяжемся и обсудим подробности', default='Ваша заявка на заморозку заказа принята, вскоре мы с вами свяжемся и обсудим подробности', max_length=200)
    get_promocode = models.CharField('Получить промокод', default='Получить промокод', max_length=200)
    get_promocode_info = models.CharField('Приведите друзей в наш сервис и мы щедро вас отблагодарим промокодом за каждого человека! Ваша реферальная ссылка: ', default='Приведите друзей в наш сервис и мы щедро вас отблагодарим промокодом за каждого человека! Ваша реферальная ссылка: ', max_length=1000)
    copy_referral_link = models.CharField('Скопировать ссылку', default='Скопировать ссылку', max_length=200)
    referral_link_copy_success = models.CharField('Ссылка скопирована', default='Ссылка скопирована', max_length=200)
    referral_link_copy_success_info = models.CharField('Реферальная ссылка успешно скопирована!', default='Реферальная ссылка успешно скопирована!', max_length=200)

    active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Пресет настройки личного кабинета'
        verbose_name_plural = 'Настройки личного кабинета'

    def save(self, *args, **kwargs):
        if self.active:
            AccountPageSettings.objects.filter(active=self.active).update(active=False)
        super(AccountPageSettings, self).save(*args, **kwargs)

    def __str__(self):
        if self.active:
            return 'Активный пресет настроек'
        else:
            return 'Пресет настроек %s' % self.id


class Question(models.Model):
    """ Вопрос """
    question = models.CharField('Вопрос', max_length=120)
    answer = RichTextField('Ответ')
    order = models.PositiveIntegerField('Порядковый номер')
    about_freeze = models.BooleanField('О заморозке', default=False)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.about_freeze:
            Question.objects.filter(about_freeze=True).update(about_freeze=False)
        super(Question, self).save(*args, **kwargs)


class QuestionBlock(models.Model):
    """ Блок вопросов """
    name = models.CharField('Название', max_length=30)
    icon = models.CharField('Иконка (класс fontawesome 5)', max_length=40)
    questions = models.ManyToManyField(Question, verbose_name='Вопросы', blank=True, null=True)
    active = models.BooleanField('Активно', default=False)

    class Meta:
        verbose_name = 'Блок частых вопросов'
        verbose_name_plural = 'Блоки частых вопросов'

    def __str__(self):
        return 'Блок вопросов %s - %s' % (self.name, ('Активен' if self.active else 'Неактивен'))


class Review(models.Model):
    """ Отзыв """
    name = models.CharField('Имя и фамилия автора отзыва', max_length=30, null=True, blank=True)
    content = models.TextField('Отзыв')
    photo = models.ImageField('Фото автора отзыва', help_text='Рекомендуемо: 200x200, формат webp',
                              upload_to='reviews/',
                              null=True, blank=True)
    photo_webp = models.ImageField('Фото автора отзыва webp', help_text='Рекомендуемо: 200x200, формат webp',
                                   upload_to='reviews/',
                                   null=True, blank=True, editable=False)
    url = models.CharField('Ссылка на автора отзыва', max_length=200)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    is_moderated = models.BooleanField('Одобрен', default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Отзыв %s' % self.created.strftime('%H:%M:%S %d/%m/%Y')


@receiver(pre_save, sender=Review)
def review_settings_pre_save(sender, instance, **kwargs):
    if instance.photo:
        add_webp_image(instance.photo, instance.photo_webp)


@receiver(post_save, sender=Review)
def compress_images(sender, instance, **kwargs):
    if instance.photo:
        img = Image.open(instance.photo.path)
        img.thumbnail((200, 200))
        img.save(instance.photo.path + '.png', 'PNG')


class Profile(models.Model):
    """ Профиль """
    STATUS_CHOICES = [
        ('activation', 'Отправленна ссылка активации'),
        ('active', 'Активен'),
        ('ban', 'Забанен'),
    ]
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('he', 'Иврит'),
    ]
    SEX_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    referral_id = models.IntegerField('ID профиля реферала', null=True, blank=True)
    name = models.CharField('Имя', max_length=150, null=True, blank=True)
    surname = models.CharField('Фамилия', max_length=150, null=True, blank=True)
    sex = models.CharField('Пол', default='male', max_length=6, choices=SEX_CHOICES)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    phone = models.CharField('Телефон', max_length=150, null=True, blank=True)
    address = models.CharField('Адрес', max_length=150, null=True, blank=True)
    status = models.CharField('Статус', default='activation', max_length=10, choices=STATUS_CHOICES)
    language = models.CharField('Язык', default='ru', max_length=2, choices=LANGUAGE_CHOICES)
    is_moderator = models.BooleanField('Модератор', default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = self.user.username
        super().save(*args, **kwargs)


class PromoCode(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='Принадлежит профилю', on_delete=models.CASCADE)
    sale = models.IntegerField('Скидка', null=True, blank=True)
    code = models.CharField('Код', unique=True, max_length=6, null=True, blank=True)
    for_all = models.BooleanField('Для всех', default=False)

    def save(self, *args, **kwargs):
        code = self.code
        if not len(code):
            allowed_chars = 'ABCDEFGH23456789'
            code = ''
            for i in range(8):
                code += allowed_chars[random.randint(0, len(allowed_chars))]
        while not PromoCode.objects.filter(code=code):
            allowed_chars = 'ABCDEFGH23456789'
            code = ''
            for i in range(8):
                code += allowed_chars[random.randint(0, len(allowed_chars))]
        self.code = code
        if not self.sale:
            self.sale = Fixed.objects.get(active=True).promocode_sale
        if self.sale <= 0:
            self.sale = 1
        if self.sale >= 100:
            self.sale = 99
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Промокод {self.code}'

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class EmailVerification(models.Model):
    """ Ключи подтверждения email """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    new_email = models.EmailField('Новый e-mail', max_length=120)
    key = models.CharField('Ключ подтверждения', max_length=6)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    def save(self, *args, **kwargs):
        key_int = random.randint(1, 1000000)
        self.key = '{:06}'.format(key_int)
        print(self.key)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Ключ подверждения email'
        verbose_name_plural = 'Ключи подверждения email'


class ResetPasswordVerification(models.Model):
    """ Ключи подтверждения сброса пароля """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    key = models.CharField('Ключ подтверждения', max_length=6)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    def save(self, *args, **kwargs):
        key_int = random.randint(1, 1000000)
        self.key = '{:06}'.format(key_int)
        print(self.key)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Ключ подверждения сброса пароля'
        verbose_name_plural = 'Ключи подверждения сброса пароля'


class ChangePersonalDataRequest(models.Model):
    """ Запрос смены личных данных """
    TYPE_CHOICES = [
        ('name', 'Имя'),
        ('surname', 'Фамилия'),
        ('phone', 'Телефон'),
        ('address', 'Адрес'),
    ]
    profile = models.ForeignKey(Profile, verbose_name='Профиль', on_delete=models.CASCADE)
    new = models.CharField('Новые данные', max_length=20)
    type = models.CharField('Тип', default='name', max_length=13, choices=TYPE_CHOICES)
    done = models.BooleanField('Выполнить', default=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.done:
            if self.type == 'name':
                self.profile.name = self.new
            if self.type == 'surname':
                self.profile.surname = self.new
            if self.type == 'phone':
                self.profile.phone = self.new
            if self.type == 'address':
                self.profile.address = self.new
            self.profile.save()
            self.delete()

    def __str__(self):
        return '%s - %s' % (self.profile.user.username, self.id)

    class Meta:
        verbose_name = 'Запрос смены личных данных'
        verbose_name_plural = 'Запросы смены личных данных'


class CallRequest(models.Model):
    """ Запрос обратного звонка """
    name = models.CharField('Имя и фамилия', max_length=150)
    phone = models.CharField('Телефон', max_length=150)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запрос обратного звонка'
        verbose_name_plural = 'Запросы обратного звонка'

    def __str__(self):
        return 'Запрос обратного звонка %s' % self.created.strftime('%H:%M:%S %d/%m/%Y')


def get_menu_to_dishes_circle(menu, full=False):
    if full:
        return [
            menu.day1_other.all(),
            menu.day2_other.all(),
            menu.day3_other.all(),
            menu.day4_other.all(),
            menu.day5_other.all(),
            menu.day6_other.all(),
            menu.day7_other.all(),
            menu.day8_other.all(),
            menu.day9_other.all(),
            menu.day10_other.all(),
            menu.day11_other.all(),
            menu.day12_other.all(),
            menu.day13_other.all(),
            menu.day14_other.all(),
            menu.day15_other.all(),
            menu.day16_other.all(),
            menu.day17_other.all(),
            menu.day18_other.all(),
            menu.day19_other.all(),
            menu.day20_other.all(),
            menu.day21_other.all(),
            menu.day22_other.all(),
            menu.day23_other.all(),
            menu.day24_other.all(),
            menu.day25_other.all(),
            menu.day26_other.all(),
        ]
    else:
        return [
            menu.day1.all(),
            menu.day2.all(),
            menu.day3.all(),
            menu.day4.all(),
            menu.day5.all(),
            menu.day6.all(),
            menu.day7.all(),
            menu.day8.all(),
            menu.day9.all(),
            menu.day10.all(),
            menu.day11.all(),
            menu.day12.all(),
            menu.day13.all(),
            menu.day14.all(),
            menu.day15.all(),
            menu.day16.all(),
            menu.day17.all(),
            menu.day18.all(),
            menu.day19.all(),
            menu.day20.all(),
            menu.day21.all(),
            menu.day22.all(),
            menu.day23.all(),
            menu.day24.all(),
            menu.day25.all(),
            menu.day26.all(),
        ]


def get_order_to_order_dishes_circle(order, full=False):
    if full:
        return [
            order.dishes_day1.all(),
            order.dishes_day2.all(),
            order.dishes_day3.all(),
            order.dishes_day4.all(),
            order.dishes_day5.all(),
            order.dishes_day6.all(),
            order.dishes_day7.all(),
            order.dishes_day8.all(),
            order.dishes_day9.all(),
            order.dishes_day10.all(),
            order.dishes_day11.all(),
            order.dishes_day12.all(),
            order.dishes_day13.all(),
            order.dishes_day14.all(),
            order.dishes_day15.all(),
            order.dishes_day16.all(),
            order.dishes_day17.all(),
            order.dishes_day18.all(),
            order.dishes_day19.all(),
            order.dishes_day20.all(),
            order.dishes_day21.all(),
            order.dishes_day22.all(),
            order.dishes_day23.all(),
            order.dishes_day24.all(),
            order.dishes_day25.all(),
            order.dishes_day26.all(),
        ]
    else:
        return [
            order.dishes_day1,
            order.dishes_day2,
            order.dishes_day3,
            order.dishes_day4,
            order.dishes_day5,
            order.dishes_day6,
            order.dishes_day7,
            order.dishes_day8,
            order.dishes_day9,
            order.dishes_day10,
            order.dishes_day11,
            order.dishes_day12,
            order.dishes_day13,
            order.dishes_day14,
            order.dishes_day15,
            order.dishes_day16,
            order.dishes_day17,
            order.dishes_day18,
            order.dishes_day19,
            order.dishes_day20,
            order.dishes_day21,
            order.dishes_day22,
            order.dishes_day23,
            order.dishes_day24,
            order.dishes_day25,
            order.dishes_day26,
        ]


def get_menu_days_to_price(menu):
    return {
        1: menu.days1_price,
        2: menu.days2_price,
        4: menu.days4_price,
        6: menu.days6_price,
        14: menu.days14_price,
        26: menu.days26_price
    }


def get_days_circle(order, days, keys_are_dates=False):
    last_date = order.last_date
    days_circle = []
    if keys_are_dates:
        days_circle = {}
    frozen_arr = order.freezes.all().order_by('frozen_from')
    i = 0
    c = 0
    freeze_i = 0
    while i != days:
        frozen_from = False
        frozen_to = False
        if freeze_i + 1 <= len(frozen_arr):
            frozen_from = frozen_arr[freeze_i].frozen_from
            frozen_to = frozen_arr[freeze_i].frozen_to

        real_date = order.first_date + datetime.timedelta(days=c)
        if frozen_from:
            if real_date >= frozen_from:
                if frozen_to:
                    if real_date <= frozen_to - datetime.timedelta(days=1):
                        c += 1
                        if real_date == frozen_to - datetime.timedelta(days=1):
                            freeze_i += 1
                        continue

        if keys_are_dates:
            days_circle[(order.first_date + datetime.timedelta(c)).strftime('%d.%m')] = ((order.first_date - settings.FIRST_GLOBAL_DATE).days + c) % 26
        else:
            days_circle.append(((order.first_date - settings.FIRST_GLOBAL_DATE).days + c) % 26)
        last_date = real_date
        i += 1
        c += 1
    return days_circle, last_date


class OrderFreeze(models.Model):
    frozen_from = models.DateField('Заморожено от', blank=True, null=True)
    frozen_to = models.DateField('Заморожено до', blank=True, null=True)
    finished = models.BooleanField('Заморозка закончена', default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Заморозка заказа'
        verbose_name_plural = 'Заморозки заказов'

    def __str__(self):
        return f'Заморозка (не заказ) #{self.id} | {self.frozen_from} - {(self.frozen_to if self.frozen_to else "...")} | {"Заморозка завершена" if self.finished else "Заморозка в процессе"}'

    def save(self, *args, **kwargs):
        self.finished = False
        if self.frozen_to:
            if self.frozen_to <= datetime.date.today():
                self.finished = True
        super().save(*args, **kwargs)


class Order(models.Model):
    """ Заказ """
    profile = models.ForeignKey(Profile, verbose_name='Профиль', on_delete=models.CASCADE, blank=True, null=True)
    referral_id = models.IntegerField('ID профиля реферала', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=150, null=True, blank=True)
    name = models.CharField('Имя Фамилия (Отчество)', max_length=150, null=True, blank=True)
    address = models.CharField('Адрес', max_length=150, null=True, blank=True)
    comment = models.CharField('Комментарий', max_length=200, null=True, blank=True)
    email = models.EmailField('Email', max_length=150, null=True, blank=True)
    payment_type = models.CharField('Метод оплаты', choices=(('cash_delivery', 'Наличкой курьеру'), ('card_delivery', 'Картой курьеру'), ('card_phone', 'Картой по телефону')), max_length=100, default='card_phone', null=True, blank=True)
    menu = models.ForeignKey(Menu, verbose_name='Меню', on_delete=models.CASCADE)
    dishes_day1 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда первый день',
                                         related_name='dishes_day1', blank=True, null=True)
    dishes_day2 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда второй день', related_name='dishes_day2',
                                         blank=True, null=True)
    dishes_day3 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда третий день',
                                         related_name='dishes_day3', blank=True, null=True)
    dishes_day4 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда четвертый день',
                                         related_name='dishes_day4', blank=True, null=True)
    dishes_day5 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда пятый день', related_name='dishes_day5',
                                         blank=True, null=True)
    dishes_day6 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда шестой день',
                                         related_name='dishes_day6', blank=True, null=True)
    dishes_day7 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда седьмой день',
                                         related_name='dishes_day7', blank=True, null=True)
    dishes_day8 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда восьмой день',
                                         related_name='dishes_day8', blank=True, null=True)
    dishes_day9 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда девятый день',
                                         related_name='dishes_day9', blank=True, null=True)
    dishes_day10 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда десятый день',
                                          related_name='dishes_day10', blank=True, null=True)
    dishes_day11 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда одиннадцатый день',
                                          related_name='dishes_day11',
                                          blank=True, null=True)
    dishes_day12 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двенадцатый день',
                                          related_name='dishes_day12', blank=True, null=True)
    dishes_day13 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда тринадцатый день',
                                          related_name='dishes_day13', blank=True, null=True)
    dishes_day14 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда четырнадцатый день',
                                          related_name='dishes_day14', blank=True, null=True)
    dishes_day15 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда пятнадцатый день',
                                          related_name='dishes_day15', blank=True, null=True)
    dishes_day16 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда шестнадцатый день',
                                          related_name='dishes_day16', blank=True, null=True)
    dishes_day17 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда семнадцатый день',
                                          related_name='dishes_day17', blank=True, null=True)
    dishes_day18 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда восемнадцатый день',
                                          related_name='dishes_day18', blank=True, null=True)
    dishes_day19 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда девятнадцатый день',
                                          related_name='dishes_day19', blank=True, null=True)
    dishes_day20 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцатый день',
                                          related_name='dishes_day20', blank=True, null=True)
    dishes_day21 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать первый день',
                                          related_name='dishes_day21', blank=True, null=True)
    dishes_day22 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать второй день',
                                          related_name='dishes_day22', blank=True, null=True)
    dishes_day23 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать третий день',
                                          related_name='dishes_day23', blank=True, null=True)
    dishes_day24 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать четвертый день',
                                          related_name='dishes_day24', blank=True, null=True)
    dishes_day25 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать пятый день',
                                          related_name='dishes_day25', blank=True, null=True)
    dishes_day26 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать шестой день',
                                          related_name='dishes_day26', blank=True, null=True)
#dishes_day27 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать седьмой день',
#                                          related_name='dishes_day27', blank=True, null=True)
#    dishes_day28 = models.ManyToManyField(Dish, verbose_name='Выбранные блюда двадцать восьмой день',
#                                          related_name='dishes_day28', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, blank=True, null=True)
    first_date = models.DateField('Первая дата', help_text='Включительно')
    days = models.IntegerField('Дней')
    last_date = models.DateField('Последняя дата', help_text='Включительно', blank=True, null=True)
    is_completed = models.BooleanField('Обработан', default=False)
    is_payed = models.BooleanField('Оплачено', default=False)
    changed_menu = models.BooleanField('Измененное меню', default=False, editable=False)
    to_return = models.IntegerField('Вернуть', blank=True, null=True, editable=False)
    extend_allowed = models.BooleanField('Разрешено продление', default=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    freezes = models.ManyToManyField(OrderFreeze, verbose_name='Заморозки', blank=True, null=True)
    promocode_sale = models.IntegerField('Скидка из-за промокода', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return 'Заказ %s' % self.id

    def save(self, selected_dishes=None, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.days == 1:
            self.extend_allowed = False
        if self.profile:
            if not self.name:
                self.name = self.profile.name + ' ' + self.profile.surname
            if not self.phone:
                self.phone = self.profile.phone
            if not self.email:
                self.email = self.profile.user.email
            if not self.address:
                self.address = self.profile.address

        home_settings = HomePageSettings.objects.get(active=True)
        days_to_price = get_menu_days_to_price(self.menu)
        order_dishes_circle = get_order_to_order_dishes_circle(self, False)
        dishes_allowed_circle = get_menu_to_dishes_circle(self.menu, True)
        default_dishes_circle = get_menu_to_dishes_circle(self.menu, False)
        days_circle, self.last_date = get_days_circle(self, self.days)
        if selected_dishes:
            dishes_ok = True
            for day in days_circle:
                dishes_allowed = dishes_allowed_circle[day]
                default_dishes = default_dishes_circle[day]
                order_dishes = order_dishes_circle[day]
                if str(day) in selected_dishes.keys():
                    for dish_id in selected_dishes[str(day)]:
                        if Dish.objects.filter(id=dish_id):
                            dish = Dish.objects.get(id=dish_id)
                            if dish in dishes_allowed:
                                order_dishes.add(dish)
                                continue
                        dishes_ok = False
                else:
                    for dish in default_dishes:
                        order_dishes.add(dish)
            if dishes_ok:
                price = Decimal(days_to_price[self.days])
                self.price = price
                super().save(*args, **kwargs)
                return {'success': True, 'order': self}
            else:
                return {'success': False, 'order': self}
        elif not self.changed_menu:
            order_dishes_circle = get_order_to_order_dishes_circle(self, False)
            for day in range(26):
                order_dishes_circle[day].clear()
            super().save(*args, **kwargs)
            order_dishes_circle = get_order_to_order_dishes_circle(self, False)
            print('\nsaved\n\nstarted save 2 with real dishes')
            print(days_circle)
            for day in days_circle:
                order_dishes = order_dishes_circle[day]
                default_dishes = default_dishes_circle[day]
                print(day, default_dishes)
                for dish in default_dishes:
                    print(dish.pk, dish)
                    order_dishes.add(dish)
            super().save(*args, **kwargs)
            order_dishes_circle = get_order_to_order_dishes_circle(self, False)
            for day in days_circle:
                order_dishes = order_dishes_circle[day]
                print('now:', day, order_dishes.all())
            print('saved')
            price = Decimal(days_to_price[self.days])
            if self.promocode_sale:
                price = Decimal(round(float(price) * (1-(self.promocode_sale/100)), 2))
            self.price = price
            super().save(*args, **kwargs)
            order_dishes_circle = get_order_to_order_dishes_circle(self, False)
            for day in days_circle:
                order_dishes = order_dishes_circle[day]
                print('now2:', day, order_dishes.all())
            print('saved2')
            return {'success': True, 'order': self}
        else:
            super().save(*args, **kwargs)
            return {'success': True, 'order': self}


class StatsPeriod(models.Model):
    profiles = models.PositiveIntegerField('Профилей', null=True, blank=True)
    profiles_change = models.IntegerField('Новых профилей', null=True, blank=True)
    orders = models.PositiveIntegerField('Заказов', null=True, blank=True)
    orders_change = models.PositiveIntegerField('Новых заказов', null=True, blank=True)
    avg_price = models.PositiveIntegerField('Средний чек', null=True, blank=True)
    income = models.PositiveIntegerField('Доход', null=True, blank=True)
    income_change = models.PositiveIntegerField('Новый доход', null=True, blank=True)
    date = models.DateTimeField('Дата', null=True, blank=True)
