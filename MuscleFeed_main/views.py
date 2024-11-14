
import json
import locale
import time

import smtplib, ssl
from email.message import EmailMessage

import pytz
import requests
from allauth.account.forms import ResetPasswordKeyForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import redirect
from django.template.defaultfilters import register as reg
from django.template.loader import get_template
from django.utils import timezone, translation
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from xlsxwriter import Workbook

from .forms import *
from .models import *


@reg.filter(name='split')
def slpit_filter(value, arg):
    return value.split(arg)


@reg.filter(name='weekday')
def weekday_filter(value):
    value_splt = value.split('.')
    return datetime.date(int(value_splt[2]), int(value_splt[1]), int(value_splt[0])).weekday()


@reg.filter(name='replace')
def replace_filter(string, repl):
    return string.replace(repl.split('--->')[0], repl.split('--->')[1])


@reg.filter(name='remove_minus')
def remove_minus(string):
    return str(string).replace('-', '')


@reg.filter(name='get_ordered_questions')
def get_ordered_questions(questions):
    return questions.order_by('order')


def activate_translations(request, language):
    lang = language
    if settings.LANGUAGE_COOKIE_NAME in request.session.keys():
        if request.user.is_authenticated:
            if Profile.objects.filter(user=request.user):
                profile = Profile.objects.get(user=request.user)
                if profile.language != request.session[settings.LANGUAGE_COOKIE_NAME]:
                    profile.language = lang
                    request.session[settings.LANGUAGE_COOKIE_NAME] = lang
                    profile.save()
    else:
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    request.session.save()
    translation.activate(lang)
    timezone.activate(pytz.timezone(settings.TIME_ZONE))



def send_mail(subject, template, lang, email, context_args):
    plaintext = get_template('emails/txt/{}/{}.txt'.format(lang, template))
    htmly = get_template('emails/html/{}/{}.html'.format(lang, template))
    fixed = Fixed.objects.get(active=True)
    context = {'fixed': fixed, 'MEDIA_URL': settings.MEDIA_URL}
    context.update(context_args)
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    if settings.LOCAL:
        print(f'\n\n\n'
              f'Key: {context["code"]}\n'
              f'HTML: {html_content}\n'
              f'TXT: {text_content}'
              f'\n\n\n')
    else:
        msg = EmailMultiAlternatives(subject, text_content, '{} <noreply@{}>'.format(fixed.site_name, fixed.base),
                                     [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        #msg = EmailMessage()
        #msg = f"From: {from_addr}\r\nTo: {','.join(to_addr)}\r\nSubject: {subject}\r\n"
        #msg.set_content("The body of the email is here")
        #msg["Subject"] = "An Email Alert"
        #msg_from = '{} <noreply@{}>'.format(fixed.site_name, fixed.base)
        #msg["To"] = [email]
        #server = smtplib.SMTP('smtp.gmail.com: 587')
        #server.starttls()
        #server.login(msg['From'], 'An654465nA')
        #server.sendmail(msg['From'], msg['To'], msg.as_string())
        #server.quit()
        #context=ssl.create_default_context()
        #msg = f"From: {from_addr}\r\nTo: {','.join(to_addr)}\r\nSubject: {subject}\r\n"

        #context = ssl.create_default_context()
        #with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        #    smtp.ehlo()
        #    smtp.starttls(context=context)
        #    smtp.ehlo()
        #    smtp.login(msg_from, 'bbnspatzelotizat')
            #smtp.sendmail(msg_from, [email], msg)


def send_auth_mail(request, template, user, email):
    """ Отправить email с ключем """
    EmailVerification.objects.filter(user=user).delete()
    key_model = EmailVerification.objects.create(user=user, new_email=email)
    t = WrapperTranslations.objects.get(active=True)
    lang = 'ru'
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    if template == 'signup':
        subject = t.registration
    if template == 'reset-password':
        subject = t.reset_password
    if template == 'change-email':
        subject = t.change_email
    data = {
        'code': key_model.key,
        'created': key_model.created,
    }
    send_mail(subject, template, request.session[settings.LANGUAGE_COOKIE_NAME], email, data)


def key_verification(request):
    """ Сверка ключа """
    username = request.POST.get('username')
    key = request.POST.get('key')
    if User.objects.filter(username=username):
        user = User.objects.get(username=username)
        if EmailVerification.objects.filter(user=user):
            key_model = EmailVerification.objects.get(user=user)
            new = key_model.new_email
            if key == key_model.key:
                return {'success': True, 'username': user.username, 'key': key, 'new': new}
    return {'success': False}


def send_whatsapp_message(type, phone, order=None, call_request=None):
    return
    fixed = Fixed.objects.get(active=True)
    url = f'https://api.green-api.com/waInstance{fixed.green_api_id_instance}/SendMessage/{fixed.green_api_api_token_instance}'
    chat_phone = ''.join([i for i in phone if i.isdigit()])
    if chat_phone[0] == '0':
        chat_phone = '972' + chat_phone[1:]
    chat_id = chat_phone + '@c.us'
    message = ''
    if type == 'admin_new_order':
        message = f'Поступил новый заказ: #{order.id}\nДаты заказа: {order.first_date.strftime("%d.%m.%y")}{" - " + order.last_date.strftime("%d.%m.%y") if order.first_date != order.first_date else ""}\nСумма заказа: {order.price} ₪\nВремя заказа: {order.created.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%d.%m.%y %H:%M")}'
    if type == 'admin_new_call_request':
        message = f'Поступил новый запрос звонка\nИмя: {call_request.name}\nТелефон: {call_request.phone}\nВремя создания: {call_request.created.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%d.%m.%y %H:%M")}'
    if type == 'admin_freeze_request':
        message = f'Поступил новый запрос на заморозку\nИмя: {order.name}\nТелефон: {order.phone}\nНомер заказа #{order.id}'
    if type == 'client_order_completed':
        message = f'הזמנתכם #{order.id} נקלטה במערכת \nתאריך משלוח ראשון {order.first_date.strftime("%d.%m.%y")}'
    if type == 'client_order_before_2_days_to_finish':
        message = f'לקוח יקר, הזמנתך השוטפת תיגמר בתאריך {order.last_date.strftime("%d.%m.%y")}\nלהמשך ולהארכת ההזמנה היכנס לאתר שלנו https://muscle-feed.com/he/ או התקשרו לטלפון שמספרו: {fixed.phone_number_he}'
    if type == 'client_receive_promocode':
        message = f'מזל טוב ! אחד מהחברים שלך עשה אצלנו הזמנה, לכן את/ה מקבל/ת \nהנחה על ההזמנה ההבאה שלך ! קוד הקופון \n{order.sale}% – {order.code} \nבברכה ‏Muscle Feed!'
    to_send_raw = {
        'chatId': chat_id,
        'message': message,
    }
    to_send = json.dumps(to_send_raw)
    retry = 5
    while True:
        response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=to_send)
        if response.status_code == 200 or retry == 0:
            break
        else:
            time.sleep(1)
            retry -= 1
    if not bool(retry):
        print(f'\n\rСообщение не отправлено.\n\rДанные: "{to_send}". Ответ: [{response.status_code}] {response.content}.\n\r')


def send_new_order_messages(order, completed=False):
    if not completed:
        if Fixed.objects.get(active=True).notification_mails:
            for mail in Fixed.objects.get(active=True).notification_mails.split('\n'):
                try:
                    send_mail('[Muscle Feed] Новый заказ', 'new-order', 'ru',
                              mail.replace('\r', '').replace('\n', ''), {'order': order})
                except Exception:
                    pass
        if Fixed.objects.get(active=True).notification_phones:
            for phone in Fixed.objects.get(active=True).notification_phones.split('\n'):
                send_whatsapp_message('admin_new_order', phone, order)
    else:
        send_whatsapp_message('client_order_completed', order.phone, order)



@csrf_protect
def signup(request, language, step):
    """ Регистрация """
    if step == 1:
        if 'email' in request.POST.keys():
            username = request.POST.get('email').replace('.', '_').replace('@', '_').lower()
            if User.objects.filter(username=username, is_active=False):
                user = User.objects.get(username=username, is_active=False)
                email = request.POST.get('email')
            else:
                form = SignupFormStep1(request.POST)
                if form.is_valid():
                    fc = form.cleaned_data
                    email = fc['email']
                    username = email.replace('.', '_').replace('@', '_').lower()
                    user = User.objects.create_user(username=username, email=email, password=fc['password1'])
                else:
                    return JsonResponse({**form.errors, **{'success': False}})
            user.is_active = False
            user.save()
            send_auth_mail(request, 'signup', user, email)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            form = SignupFormStep1(request.POST)
            form_invalid = form.is_valid()
            return JsonResponse({**form.errors, **{'success': False}})
    elif step == 2:
        return JsonResponse(key_verification(request))
    elif step == 3:
        username = request.POST.get('username')
        key = request.POST.get('key')
        referral_id = request.POST.get('referral_id')
        if User.objects.filter(username=username):
            form = SignupFormStep3(request.POST)
            if form.is_valid():
                user = User.objects.get(username=username)
                profile = Profile.objects.create(user=user)
                # Some safety stuff
                if EmailVerification.objects.filter(user=user, key=key):
                    user.email = EmailVerification.objects.get(user=user, key=key).new_email
                    user.is_active = True
                    user.save()
                    profile.status = 'active'
                    EmailVerification.objects.filter(user=user).delete()
                    fc = form.cleaned_data
                    profile.name = fc['user_name']
                    profile.surname = fc['user_surname']
                    profile.address = fc['user_address']
                    if referral_id:
                        if Profile.objects.filter(id=referral_id, status='active'):
                            profile.referral_id = referral_id
                    if fc['user_phone']:
                        profile.phone = fc['user_phone']
                    profile.status = 'active'
                    profile.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return JsonResponse({'success': True, 'id': user.id})
            else:
                return JsonResponse({**form.errors, **{'success': False}})
        return JsonResponse({'success': False})


@csrf_protect
def login(request, language):
    """ Вход """
    username = request.POST.get('email').replace('.', '_').replace('@', '_').lower()
    password = request.POST.get('password')
    auth_form = AuthenticationForm(request, {'username': username, 'password': password})
    if auth_form.is_valid():
        if request.POST.get('remember') == "true":
            pass
        else:
            request.session.set_expiry(0)
        user = auth.authenticate(username=username, password=password)
        profile = Profile.objects.get(user=user)
        lang = 'ru'
        if profile.language:
            lang = profile.language
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
        request.session.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        return JsonResponse({'success': True, 'id': user.id})
    else:
        return JsonResponse({'success': False})


@login_required
@csrf_protect
def logout(request, language):
    """ Выход """
    lang = Profile.objects.get(user=request.user).language
    auth.logout(request)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    request.session.save()
    translation.activate(lang)
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    return redirect('home', lang)


@csrf_protect
def reset_password(request, language, step):
    """ Сброс пароля """
    if step == 1:
        if User.objects.filter(email=request.POST.get('email'), is_active=True):
            user = User.objects.get(email=request.POST.get('email'))
            send_auth_mail(request, 'reset-password', user, user.email)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            return JsonResponse({'success': False})
    elif step == 2:
        return JsonResponse(key_verification(request))
    elif step == 3:
        username = request.POST.get('username')
        key = request.POST.get('key')
        if User.objects.filter(username=username):
            form = ResetPasswordKeyForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=username)
                # Some safety stuff
                if EmailVerification.objects.filter(user=user, key=key):
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    EmailVerification.objects.filter(user=user).delete()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return JsonResponse({'success': True, 'id': user.id})
            else:
                return JsonResponse({**form.errors, **{'success': False}})
        return JsonResponse({'success': False})


@csrf_protect
def language_change(request, language):
    lang = request.POST.get('language')
    language_list = ['he', 'ru']
    if lang in language_list:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            profile.language = lang
            profile.save()
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
        activate_translations(request, language)
        return JsonResponse({'success': True, 'lang': lang})
    return JsonResponse({'success': False})


def wrap_data(context):
    """ Функция добавления контекста wrapper """
    context['fixed'] = Fixed.objects.get(active=True)
    context['user_agreement'] = UserAgreement.objects.get(active=True)
    context['privacy_policy'] = PrivacyPolicy.objects.get(active=True)
    context['wt'] = WrapperTranslations.objects.get(active=True)
    return context


class HomePage(generic.TemplateView):
    """ Главная страница """
    template_name = 'home.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            if request.user.is_active:
                if Profile.objects.filter(user=request.user, status='active'):
                    context['address'] = Profile.objects.get(user=request.user).address
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = HomePageSettings.objects.get(active=True)
        context['reviews_count'] = False
        if Review.objects.filter(is_moderated=True).count() >= 3:
            context['reviews'] = Review.objects.filter(is_moderated=True).order_by('-created')[:3]
            context['reviews_count'] = Review.objects.filter(is_moderated=True).count()
        context['question_blocks'] = False
        if QuestionBlock.objects.filter(active=True).count():
            context['question_blocks'] = QuestionBlock.objects.filter(active=True)
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        first_date_delay = 1
        first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=first_date_delay)
        context['dates'] = [{
            'date': first_date + datetime.timedelta(i),
            'weekday': (first_date + datetime.timedelta(i)).weekday,
            'circleday': ((first_date - settings.FIRST_GLOBAL_DATE).days + i) % 26,
        } for i in range(6)]
        context['daytimes'] = ['breakfast', 'second-breakfast', 'lunch', 'high-tea', 'dinner', 'drink']
        context['menu_types'] = MenuType.objects.filter(active=True).order_by('order')
        menus = Menu.objects.filter(active=True).order_by('home_order')
        context['menus'] = menus
        menu_prices = {}
        for menu in menus:
            days_to_price = get_menu_days_to_price(menu)
            if f'menu-{menu.id}' not in menu_prices.keys():
                menu_prices[f'menu-{menu.id}'] = {}
            for days in [1, 2, 4, 6, 14, 26]:
                menu_prices[f'menu-{menu.id}'][f'days-{days}'] = days_to_price[days]
        context['menu_prices'] = menu_prices
        menus_data = {}
        menus_other_data = {}
        for menu in menus:
            dishes = get_menu_to_dishes_circle(menu, False)
            dishes_other = get_menu_to_dishes_circle(menu, True)
            if f'menu-{menu.id}' not in menus_data.keys():
                menus_data[f'menu-{menu.id}'] = {}
            if f'menu-{menu.id}' not in menus_other_data.keys():
                menus_other_data[f'menu-{menu.id}'] = {}
            for date_data in context['dates']:
                if f'circleday-{date_data["circleday"]}' not in menus_data[f'menu-{menu.id}'].keys():
                    menus_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'] = {}
                if f'circleday-{date_data["circleday"]}' not in menus_other_data[f'menu-{menu.id}'].keys():
                    menus_other_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'] = {}
                for daytime in context['daytimes']:
                    if f'daytime-{daytime}' not in menus_data[f'menu-{menu.id}'][
                        f'circleday-{date_data["circleday"]}'].keys():
                        menus_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'][f'daytime-{daytime}'] = {}
                    if f'daytime-{daytime}' not in menus_other_data[f'menu-{menu.id}'][
                        f'circleday-{date_data["circleday"]}'].keys():
                        menus_other_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'][
                            f'daytime-{daytime}'] = {}
                    for dish in dishes_other[date_data["circleday"]].filter(type=daytime):
                        dish_data = {
                            'name': dish.name,
                            'description': dish.description,
                            'calories': dish.calories,
                            'weight': dish.weight,
                            'proteins': dish.proteins,
                            'fats': dish.fats,
                            'carbohydrates': dish.carbohydrates,
                            'image_url': dish.image.url,
                            'image_webp_url': dish.image_webp.url,
                        }
                        menus_other_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'][f'daytime-{daytime}'][
                            f'dish-{dish.id}'] = dish_data
                        if dish in dishes[date_data["circleday"]]:
                            menus_data[f'menu-{menu.id}'][f'circleday-{date_data["circleday"]}'][f'daytime-{daytime}'][
                                f'dish-{dish.id}'] = dish_data
        context['menus_data'] = menus_data
        context['menus_other_data'] = menus_other_data
        context['video'] = Video.objects.filter(active=True)
        return wrap_data(context)


def reviews_show_all(request, language):
    if 'last_id' in request.GET.keys():
        last_id = request.GET['last_id']
        reviews = Review.objects.filter(is_moderated=True, id__lt=last_id).order_by('-created')
        jsoned_reviews = [{
            'url': review.url,
            'name': review.name,
            'photo_url': review.photo.url,
            'photo_webp_url': review.photo_webp.url,
            'content': review.content
        } for review in reviews]
        return JsonResponse({'success': True, 'reviews': jsoned_reviews})
    return JsonResponse({'success': False})


@csrf_protect
def write_review(request, language):
    form = WriteReviewForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@csrf_protect
def call_me(request, language):
    form = CallMeForm(request.POST)
    if form.is_valid():
        call_request = form.save()
        if Fixed.objects.get(active=True).notification_phones:
            for phone in Fixed.objects.get(active=True).notification_phones.split('\n'):
                send_whatsapp_message('admin_new_call_request', phone, None, call_request)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@csrf_protect
def make_order(request, language):
    is_phone = False
    if request.POST.get('phone'):
        is_phone = True
    days = int(request.POST.get('days'))
    menu_id = request.POST.get('menu_id')
    payment_type = request.POST.get('payment_type')
    comment = request.POST.get('comment')
    address = request.POST.get('address')
    referral_id = request.POST.get('referral_id')
    promocode = request.POST.get('promocode')
    circledays_dishes_ids = json.loads(request.POST.get('dishes'))
    if menu_id.isdigit():
        if Menu.objects.filter(id=menu_id, active=True):
            menu = Menu.objects.get(id=menu_id, active=True)
            day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
            first_date_delay = 1
            first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(
                days=first_date_delay)
            new_order = Order(
                menu=menu,
                comment=comment,
                address=address,
                first_date=first_date,
                days=days,
                payment_type=payment_type
            )
            new_order.name = request.POST.get('name')
            if is_phone:
                new_order.phone = request.POST.get('phone')
            if request.user.is_authenticated:
                if Profile.objects.filter(user=request.user):
                    profile = Profile.objects.get(user=request.user)
                    new_order.profile = profile
                    new_order.email = profile.user.email
                    name = profile.name + ' ' + profile.surname
                    new_order.name = name
                    # Send payment mail
            if promocode:
                if PromoCode.objects.filter(code=promocode, for_all=True):
                    promocode_obj = PromoCode.objects.get(code=promocode, for_all=True)
                    new_order.promocode_sale = promocode_obj.sale
                else:
                    if request.user.is_authenticated:
                        if PromoCode.objects.filter(profile=profile, code=promocode):
                            promocode_obj = PromoCode.objects.get(profile=profile, code=promocode)
                            new_order.promocode_sale = promocode_obj.sale
                            promocode_obj.delete()
            true_referral_id = None
            if referral_id:
                true_referral_id = referral_id
            else:
                if request.user.is_authenticated:
                    if Profile.objects.filter(user=request.user, status='active'):
                        profile = Profile.objects.get(user=request.user, status='active')
                        if profile.referral_id:
                            true_referral_id = profile.referral_id
            referral_id = true_referral_id
            true_referral_id = None
            if request.user.is_authenticated:
                if Profile.objects.filter(user=request.user, status='active'):
                    profile = Profile.objects.get(user=request.user, status='active')
                    if profile.id != referral_id:
                        true_referral_id = referral_id
            else:
                true_referral_id = referral_id
            referral_id = true_referral_id
            true_referral_id = None
            if Profile.objects.filter(id=referral_id, status='active'):
                profile = Profile.objects.get(id=referral_id, status='active')
                if profile.phone != new_order.phone:
                    true_referral_id = referral_id
            if true_referral_id:
                new_order.referral_id = true_referral_id
            new_order_response = new_order.save(circledays_dishes_ids)
            if new_order_response:
                send_new_order_messages(new_order, False)
                return JsonResponse({'success': True, 'new_order_id': new_order.id, 'new_order_price': new_order.price,
                     'dishes_ok': True})
            else:
                return JsonResponse({'success': True, 'dishes_ok': False})
    return JsonResponse({'success': False})


def generate_orders_json(orders_qs, moderate=False):
    if not moderate:
        all_orders_loaded = True
        if len(orders_qs) > 40:
            all_orders_loaded = False
            orders_qs = orders_qs[:40]
    day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
    first_date_delay = 1
    allowed_change_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=first_date_delay)
    orders = {}
    for i, order in enumerate(orders_qs):
        frozen_from = False
        frozen_to = False
        if order.freezes.filter(finished=False):
            freeze_last = order.freezes.get(finished=False)
            frozen_from = freeze_last.frozen_from
            if freeze_last.frozen_to:
                if freeze_last.frozen_to <= datetime.date.today():
                    freeze_last.finished = True
                    freeze_last.save()
                    order.save()
                    frozen_from = False
                    frozen_to = False
                else:
                    frozen_to = freeze_last.frozen_to
        freeze_allowed = False
        if order.days != 1:
            if frozen_from:
                if frozen_from > datetime.date.today():
                    freeze_allowed = True
            else:
                freeze_allowed = True
        frozen = False
        if frozen_from:
            if datetime.date.today() >= frozen_from:
                frozen = True
        if frozen_from:
            frozen_from = frozen_from.strftime('%e.%m.%Y')
        if frozen_to:
            frozen_to = frozen_to.strftime('%e.%m.%Y')
        orders[i] = {
            'menu': {
                'id': order.menu.id,
                'parent_id': order.menu.type.id,
                'name': order.menu.name,
                'calories': order.menu.calories,
                'description': order.menu.description
            },
            'id': order.id,
            'is_payed': order.is_payed,
            'first_date': order.first_date.strftime('%e.%m.%Y'),
            'days': order.days,
            'last_date': order.last_date.strftime('%e.%m.%Y'),
            'allowed_menu_change': order.last_date >= allowed_change_date,
            'changed_menu': order.changed_menu,
            'extend_allowed': order.extend_allowed,
            'to_return': order.to_return,
            'freeze_allowed': freeze_allowed,
            'frozen': frozen,
            'frozen_from': frozen_from,
            'frozen_to': frozen_to,
            'close_to_finish': datetime.date.today() + datetime.timedelta(days=1) == order.last_date or datetime.date.today() == order.last_date,
            'waiting': order.first_date > datetime.date.today(),
        }
        if moderate:
            orders[i] = {**orders[i], **{
                'created': order.created.strftime('%e.%m.%Y %H:%S'),
                'name': order.name,
                'phone': order.phone,
                'price': order.price,
                'email': order.email,
                'address': order.address,
                'comment': order.comment,
                'payment_type': order.payment_type
            }}
    if moderate:
        return {'orders': orders}
    else:
        return {
            'orders': orders,
            'all_orders_loaded': all_orders_loaded
        }


class AccountPage(generic.TemplateView):
    """ Странциа аккаунта """
    template_name = 'account.html'

    def get(self, request, **kwargs):
        user_id = int(self.kwargs['id'])
        if request.user.id == user_id \
                and User.objects.get(id=user_id).is_active \
                and Profile.objects.get(user_id=user_id).status == 'active':
            # Some security stuff
            is_moderator = Profile.objects.get(user_id=user_id).is_moderator
            context = self.get_context_data_meta()
            if is_moderator:
                self.get_context_data_moderator(context)
            else:
                self.get_context_data_default(context)
            return self.render_to_response(context)
        else:
            return redirect('home')

    def get_context_data_meta(self):
        """ Общий контекст для страницы аккаунта """
        context = super().get_context_data()
        context['page'] = AccountPageSettings.objects.get(active=True)
        context['home_page'] = HomePageSettings.objects.get(active=True)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['today'] = datetime.date.today()
        context['menu_types'] = MenuType.objects.filter(active=True).order_by('order')
        menus = Menu.objects.filter(active=True).order_by('home_order')
        context['menus'] = menus
        context['freeze_min_date'] = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%e.%m.%Y')
        return wrap_data(context)

    def get_context_data_default(self, context):
        """ Контекст для страницы аккаунта пользователя """
        orders_qs = Order.objects.filter(
            profile=context['profile']
        ).union(Order.objects.filter(
            phone=context['profile'].phone
        )).order_by('-created')
        json_orders = generate_orders_json(orders_qs)
        context['orders'] = json_orders['orders']
        context['all_orders_loaded'] = json_orders['all_orders_loaded']

    def get_context_data_moderator(self, context):
        """ Контекст для страницы аккаунта модератора """
        last_date = timezone.localtime() - datetime.timedelta(days=90)
        context['change_requests'] = ChangePersonalDataRequest.objects.all().order_by('-created')
        context['call_requests'] = CallRequest.objects.all().order_by('-created')
        context['review_requests'] = Review.objects.filter(is_moderated=False).order_by('-created')
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=1)
        context['first_date'] = first_date
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        allowed_menu_change = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=2)
        context['allowed_menu_change'] = allowed_menu_change
        orders_completed_qs = Order.objects.filter(created__gte=last_date, is_completed=True).order_by('-created')
        context['orders'] = {
            'not_completed': Order.objects.filter(
                is_completed=False,
            ).order_by('-created'),
            'completed': generate_orders_json(orders_completed_qs, True)['orders'],
        }
        home_settings = HomePageSettings.objects.get(active=True)
        context['orders_not_payed_count'] = len(orders_completed_qs.filter(is_payed=False))
        orders_active_count = 0
        orders_frozen_count = 0
        orders_finished_count = 0
        orders_close_to_finish_count = 0
        orders_waiting_count = 0
        for order in orders_completed_qs:
            frozen_from = False
            frozen_to = False
            if order.freezes.filter(finished=False):
                freeze_last = order.freezes.get(finished=False)
                frozen_from = freeze_last.frozen_from
                if freeze_last.frozen_to:
                    if freeze_last.frozen_to <= context['today']:
                        freeze_last.finished = True
                        freeze_last.save()
                        order.save()
                        frozen_from = False
                        frozen_to = False
                    else:
                        frozen_to = freeze_last.frozen_to
            frozen = False
            if frozen_from:
                frozen = True
            if frozen:
                orders_frozen_count += 1
            else:
                if order.first_date <= context['today'] <= order.last_date:
                    orders_active_count += 1
                if order.last_date < context['today']:
                    orders_finished_count += 1
                if order.first_date > context['today']:
                    orders_waiting_count += 1
                if order.last_date == context['today'] + datetime.timedelta(days=1) or order.last_date == context['today']:
                    orders_close_to_finish_count += 1
        context['orders_active_count'] = orders_active_count
        context['orders_frozen_count'] = orders_frozen_count
        context['orders_finished_count'] = orders_finished_count
        context['orders_close_to_finish_count'] = orders_close_to_finish_count
        context['orders_waiting_count'] = orders_waiting_count


@csrf_protect
@login_required
def account_order_freeze(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        moderator = False
        order = None
        if profile.is_moderator and Order.objects.filter(id=order_id):
            order = Order.objects.get(id=order_id)
            profile = order.profile
            moderator = True
        elif Order.objects.filter(id=order_id, profile=profile):
            order = Order.objects.get(id=order_id, profile=profile)
        if order:
            if moderator:
                date_split = request.POST.get('date').split('.')
                date = datetime.date(int(date_split[2]), int(date_split[1]), int(date_split[0]))
                tomorrow = (date + datetime.timedelta(days=1))
                tomorrow_str = f'{tomorrow.day}.{tomorrow.month}.{tomorrow.year}'
                if order.freezes.filter(finished=False):
                    freeze = order.freezes.get(finished=False)
                    freeze_allowed = False
                    if order.days != 1:
                        if freeze.frozen_from:
                            if freeze.frozen_from > datetime.date.today():
                                freeze_allowed = True
                        else:
                            freeze_allowed = True
                    if freeze_allowed and datetime.date.today() < date <= order.last_date:
                        freeze.frozen_from = date
                        freeze.save()
                        order.save()
                        return JsonResponse({'success': True, 'unfreeze_allowed_from': tomorrow_str})
                else:
                    if order.days != 1 and datetime.date.today() < date <= order.last_date:
                        freeze = OrderFreeze.objects.create(frozen_from=date)
                        order.freezes.add(freeze)
                        order.save()
                        return JsonResponse({'success': True, 'unfreeze_allowed_from': tomorrow_str})
            else:
                if Fixed.objects.get(active=True).notification_phones:
                    for phone in Fixed.objects.get(active=True).notification_phones.split('\n'):
                        send_whatsapp_message('admin_freeze_request', phone, order)
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_unfreeze(request, language, id):
    if request.POST.get('order_id') and request.POST.get('date'):
        order_id = int(request.POST.get('order_id'))
        date_split = request.POST.get('date').split('.')
        date = datetime.date(int(date_split[2]), int(date_split[1]), int(date_split[0]))
        profile = Profile.objects.get(user=request.user)
        order = None
        if profile.is_moderator and Order.objects.filter(id=order_id):
            order = Order.objects.get(id=order_id)
        if order:
            if order.freezes.filter(finished=False):
                freeze = order.freezes.get(finished=False)
                if freeze.frozen_from:
                    unfrozen_from_allowed = freeze.frozen_from
                    if date >= unfrozen_from_allowed:
                        freeze.frozen_to = date
                        freeze.save()
                        order.save()
                        return JsonResponse({'success': True, 'last_date': order.last_date.strftime('%e.%m.%Y')})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_delete_freeze(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        if profile.is_moderator and Order.objects.filter(id=order_id):
            order = Order.objects.get(id=order_id)
            order.freezes.filter(finished=False).delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_load_orders(request, language, id):
    if request.POST.get('last_order_id'):
        last_order_id = int(request.POST.get('last_order_id'))
        profile = Profile.objects.get(user=request.user)
        orders_qs = Order.objects.filter(
            profile=profile,
            id__lt=last_order_id
        ).union(Order.objects.filter(
            phone=profile.phone,
            id__lt=last_order_id
        )).order_by('-created')
        json_orders = generate_orders_json(orders_qs)
        return JsonResponse({
            'success': True,
            'orders': json_orders['orders'],
            'today': datetime.date.today().strftime('%e.%m.%Y'),
            'all_orders_loaded': json_orders['all_orders_loaded']
        })


@csrf_protect
@login_required
def account_order_extend_load(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        order = None
        if profile.is_moderator and Order.objects.filter(id=order_id, extend_allowed=True):
            order = Order.objects.get(id=order_id, extend_allowed=True)
        elif Order.objects.filter(id=order_id, profile=profile, extend_allowed=True):
            order = Order.objects.get(id=order_id, profile=profile, extend_allowed=True)
        if order:
            day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
            first_date_delay = 1
            first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=first_date_delay)
            if order.last_date >= datetime.date.today():
                first_date = order.last_date + datetime.timedelta(days=1)
            days_to_price = get_menu_days_to_price(order.menu)
            home_settings = HomePageSettings.objects.get(active=True)
            price_list = {}
            dishes_ok = True
            for days in [2, 4, 6, 14, 26]:
                days_circle, last_date = get_days_circle(order, order.days)
                price = Decimal(days_to_price[days])
                price_list[days] = price
            return JsonResponse({'success': True, 'price_list': price_list, 'dishes_ok': dishes_ok})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_extend(request, language, id):
    if request.POST.get('order_id') and request.POST.get('days'):
        order_id = int(request.POST.get('order_id'))
        days = int(request.POST.get('days'))
        profile = Profile.objects.get(user=request.user)
        moderator = False
        order = None
        if profile.is_moderator and Order.objects.filter(id=order_id, extend_allowed=True):
            order = Order.objects.get(id=order_id, extend_allowed=True)
            profile = order.profile
            moderator = True
        elif Order.objects.filter(id=order_id, profile=profile, extend_allowed=True):
            order = Order.objects.get(id=order_id, profile=profile, extend_allowed=True)
        if order and days in [2, 4, 6, 14, 26]:
            day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
            first_date_delay = 1
            first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=first_date_delay)
            if order.last_date >= datetime.date.today():
                first_date = order.last_date + datetime.timedelta(days=1)
            new_order = Order(
                profile=profile,
                phone=order.phone,
                email=order.email,
                name=order.name,
                address=order.address,
                comment=order.comment,
                menu=order.menu,
                first_date=first_date,
                days=days,
                payment_type=order.payment_type
            )
            if moderator:
                new_order.is_completed = True
            # Send payment mail
            new_order = new_order.save()
            if new_order['success']:
                send_new_order_messages(order, False)
                return JsonResponse({
                    'success': True,
                    'order': generate_orders_json(Order.objects.filter(id=new_order['order'].id), moderator)['orders'][0],
                    'to_pay': order.price,
                    'today': datetime.date.today().strftime('%e.%m.%Y'),
                    'dishes_ok': True
                })
            else:
                return JsonResponse({'success': True, 'dishes_ok': False})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_show_dishes(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        order = None
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        allowed_change_date = datetime.datetime(int(year), int(month), int(day))
        if profile.is_moderator:
            order = Order.objects.get(id=order_id)
        elif Order.objects.filter(id=order_id, profile=profile):
            order = Order.objects.get(id=order_id, profile=profile)
            allowed_change_date = datetime.datetime(int(year), int(month), int(day)) + datetime.timedelta(days=3)
        if order:
            order_dishes_circle = get_order_to_order_dishes_circle(order, True)
            all_dishes_circle = get_menu_to_dishes_circle(order.menu, True)
            home_settings = HomePageSettings.objects.get(active=True)
            daytime_translate = {
                'drink': home_settings.drink,
                'breakfast': home_settings.breakfast,
                'second-breakfast': home_settings.second_breakfast,
                'lunch': home_settings.lunch,
                'high-tea': home_settings.high_tea,
                'dinner': home_settings.dinner,
            }
            dishes_all = {}
            dishes_now = {}
            days_circle, last_date = get_days_circle(order, order.days, True)
            for date_str, circleday in days_circle.items():
                date = datetime.datetime(datetime.date.today().year, int(date_str.split('.')[1]), int(date_str.split('.')[0]))
                weekday = date.weekday()
                if all_dishes_circle[circleday]:
                    dishes_all[date_str] = {f'circleday-{circleday}': {'weekday': weekday}}
                    dishes_now[date_str] = {f'circleday-{circleday}': {'weekday': weekday}}
                    for daytime in daytime_translate.keys():
                        if daytime not in dishes_all[date_str][f'circleday-{circleday}'].keys():
                            dishes_all[date_str][f'circleday-{circleday}'][f'daytime-{daytime}'] = []
                        if daytime not in dishes_now[date_str][f'circleday-{circleday}'].keys():
                            dishes_now[date_str][f'circleday-{circleday}'][f'daytime-{daytime}'] = []
                        for dish in all_dishes_circle[circleday].filter(type=daytime):
                            dish_data = {
                                'id': dish.id,
                                'name': dish.name,
                                'description': dish.description,
                                'calories': dish.calories,
                                'weight': dish.weight,
                                'image_url': dish.image.url,
                                'image_webp_url': dish.image_webp.url,
				'fats': dish.fats,
				'proteins': dish.proteins,
				'carbohydrates': dish.carbohydrates,
                            }
                            #if date >= allowed_change_date:
                            dishes_all[date_str][f'circleday-{circleday}'][f'daytime-{daytime}'].append(dish_data)
                            if dish in order_dishes_circle[circleday].filter(type=daytime):
                                dishes_now[date_str][f'circleday-{circleday}'][f'daytime-{daytime}'].append(dish_data)
            return JsonResponse({'success': True, 'dishes_all': dishes_all, 'dishes_now': dishes_now,
                                 'daytime_translate': daytime_translate})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_change_dish(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        this_year = datetime.date(int(year) - 1, 6, 1)
        order = None
        allowed_change_date = datetime.date(int(year), int(month), int(day))
        if profile.is_moderator:
            order = Order.objects.get(id=order_id, created__gt=this_year)
        elif Order.objects.filter(id=order_id, profile=profile, created__gt=this_year):
            order = Order.objects.get(id=order_id, profile=profile, created__gt=this_year)
            allowed_change_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=3)
        if order:
            date_recieved = request.POST.get('date')
            last_dish_id = int(request.POST.get('last_dish_id'))
            new_dish_id = int(request.POST.get('new_dish_id'))
            order_dishes_circle = get_order_to_order_dishes_circle(order, False)
            all_dishes_circle = get_menu_to_dishes_circle(order.menu, True)
            days_circle, last_date = get_days_circle(order, order.days, True)
            for date_str, circleday in days_circle.items():
                if date_str == date_recieved:
                    #if datetime.date(int(year), int(date_str.split('.')[1]), int(date_str.split('.')[0])) >= allowed_change_date:
                        order_dishes = order_dishes_circle[circleday]
                        if order_dishes.filter(id=last_dish_id):
                            last_dish = order_dishes.get(id=last_dish_id)
                            new_dish = Dish.objects.get(id=new_dish_id)
                            if new_dish in all_dishes_circle[circleday]:
                                order_dishes.remove(last_dish)
                                order_dishes.add(new_dish)
                                return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_change_menu_calculate(request, language, id):
    if request.POST.get('order_id') and request.POST.get('menu_id') and request.POST.get('days'):
        order_id = int(request.POST.get('order_id'))
        menu_id = int(request.POST.get('menu_id'))
        days_get = int(request.POST.get('days'))
        profile = Profile.objects.get(user=request.user)
        if profile.is_moderator:
            order = Order.objects.get(id=order_id)
            profile = order.profile
        print(0)
        if Order.objects.filter(id=order_id, profile=profile):
            print('0.5')
            order = Order.objects.get(id=order_id, profile=profile)
            home_settings = HomePageSettings.objects.get(active=True)
            day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
            allowed_change_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=3)
            days_not_allowed = []
            days_gone = (allowed_change_date - order.first_date).days
            taken_price = Decimal(0.00)
            if days_gone > 0:
                days_change = (allowed_change_date - order.first_date).days
                if days_change <= 1:
                    days_change = 1
                elif days_change <= 2:
                    days_change = 2
                elif days_change <= 4:
                    days_change = 4
                elif days_change <= 6:
                    days_change = 6
                elif days_change <= 14:
                    days_change = 14
                elif days_change <= 26:
                    days_change = 26
                days_to_price = get_menu_days_to_price(order.menu)
                taken_price = Decimal(days_to_price[days_change])
            for day in [1, 2, 4, 6, 14, 26]:
                if day <= days_gone:
                    days_not_allowed.append(day)
            if Menu.objects.filter(id=menu_id, active=True):
                menu = Menu.objects.get(id=menu_id, active=True)
                print(2)
                if menu.type == order.menu.type:
                    print(2)
                    if order.days == days_get and order.menu == menu:
                        return JsonResponse({'success': True, 'allowed': False, 'days_not_allowed': days_not_allowed,
                                             'price_change': 0})
                    price = Decimal(0.00)
                    if days_get > days_gone and days_get in [1, 2, 4, 6, 14, 26]:
                        days_to_price = get_menu_days_to_price(order.menu)
                        price = Decimal(days_to_price[days_get])
                        allowed = True
                        price_change = order.price - (price - taken_price)
                        if price_change > 0:
                            price_change = 0
                        return JsonResponse({'success': True, 'allowed': allowed, 'days_not_allowed': days_not_allowed, 'price_change': price_change})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_change_menu_submit(request, language, id):
    if request.POST.get('order_id') and request.POST.get('menu_id') and request.POST.get('days'):
        order_id = int(request.POST.get('order_id'))
        menu_id = request.POST.get('menu_id')
        days_get = int(request.POST.get('days'))
        print(1)
        profile = Profile.objects.get(user=request.user)
        if profile.is_moderator:
            order = Order.objects.get(id=order_id)
            profile = order.profile
        if Order.objects.filter(id=order_id, profile=profile):
            print(2)
            order = Order.objects.get(id=order_id, profile=profile)
            home_settings = HomePageSettings.objects.get(active=True)
            day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
            allowed_change_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=3)
            days_not_allowed = []
            days_gone = (allowed_change_date - order.first_date).days
            taken_price = Decimal(0.00)
            if days_gone > 0:
                days_change = days_gone
                if days_change <= 1:
                    days_change = 1
                elif days_change <= 2:
                    days_change = 2
                elif days_change <= 4:
                    days_change = 4
                elif days_change <= 6:
                    days_change = 6
                elif days_change <= 14:
                    days_change = 14
                elif days_change <= 26:
                    days_change = 26
                days_to_price = get_menu_days_to_price(order.menu)
                taken_price = Decimal(days_to_price[days_change])
            for day in [1, 2, 4, 6, 14, 26]:
                if day <= days_gone:
                    days_not_allowed.append(day)
            if Menu.objects.filter(id=menu_id, active=True):
                menu = Menu.objects.get(id=menu_id, active=True)
                if menu.type == order.menu.type:
                    print(4)
                    if order.days == days_get and order.menu == menu:
                        return JsonResponse({'success': False})
                    print(5)
                    if len(days_not_allowed) == 0:
                        order.menu = menu
                        order.days = days_get
                        order = order.save()
                        return JsonResponse({'success': order['success']})
                    elif days_get > days_gone and days_get in [1, 2, 4, 6, 14, 26]:
                        days_to_price = get_menu_days_to_price(order.menu)
                        price = Decimal(days_to_price[days_get])
                        order.to_return = order.price - (price - taken_price)
                        if order.to_return > 0:
                            order.to_return = 0
                        order_dishes_circle = get_order_to_order_dishes_circle(order, False)
                        default_dishes_circle = get_menu_to_dishes_circle(menu, False)
                        days_circle, last_date = get_days_circle(order, days_get)
                        for day in days_circle:
                            for dish in order_dishes_circle[day].all():
                                order_dishes_circle[day].remove(dish)
                            for dish in default_dishes_circle[day].all():
                                order_dishes_circle[day].add(dish)

                        order.changed_menu = True
                        order.days = days_get
                        order.last_date = order.first_date + datetime.timedelta(days=order.days - 1)
                        order.menu = menu
                        order = order.save()
                        return JsonResponse({'success': order['success']})
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_order_pay_info(request, language, id):
    if request.POST.get('order_id'):
        order_id = int(request.POST.get('order_id'))
        profile = Profile.objects.get(user=request.user)
        if Order.objects.filter(id=order_id, profile=profile):
            order = Order.objects.get(id=order_id, profile=profile)
            while True:
                token_values = {
                    'id': settings.PAYMENT_ID,
                    'secret': settings.PAYMENT_SECRET,
                }
                token_headers = {
                    'Content-Type': 'application/json'
                }
                token_request = requests.post(f'https://{("sandbox.d" if settings.LOCAL else "api")}.greeninvoice.co.il/api/v1/account/token',
                                  data=json.dumps(token_values), headers=token_headers)
                if token_request.status_code == requests.codes.ok:
                    break
            token = token_request.json()['token']
            values = {
                'description': f'Order #{order.id}',
                'type': 320,
                'lang': ('he' if profile.language == 'he' else 'en'),
                'currency': 'ILS',
                'vatType': 0,
                'amount': float(order.price),
                'maxPayments': 1,
                'client': {
                    'id': f'{order.profile.id}',
                    'name': f'{order.name}',
                    'emails': [
                        f'{order.profile.user.email}'
                    ],
                    'phone': f'{order.phone}',
                    'add': True,
                },
                'income': [
                    {
                        'description': f'{order.menu.name}, {order.first_date} - {order.last_date}',
                        'quantity': 1,
                        'price': float(order.price),
                        'currency': 'ILS',
                        'vatType': 0
                    }
                ],
                'remarks': f'Delivery address: {order.address}, Additional info: {order.comment}',
                'successUrl': f'https://muscle-feed.com/{profile.language}/user-{profile.user.id}/#SuccessfulPayment?id={order.id}',
                'failureUrl': f'https://muscle-feed.com/{profile.language}/user-{profile.user.id}/#FailurePayment?id={order.id}',
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer JWT',
                'X-Authorization-Bearer': token,
            }
            request_iframe_link = requests.post(f'https://{("sandbox.d" if settings.LOCAL else "api")}.greeninvoice.co.il/api/v1/payments/form',
                              data=json.dumps(values), headers=headers)
            print(response_iframe_link.status_code, response_iframe_link.json())
            if request_iframe_link.status_code == requests.codes.ok:
                response_iframe_link = request_iframe_link.json()
                if response_iframe_link['errorCode'] == 0:
                    print(response_iframe_link['url'])
                    return JsonResponse({
                        'success': True,
                        'payment_url': response_iframe_link['url'],
                    })
    return JsonResponse({'success': False})


@csrf_protect
@login_required
def account_change_password(request, language, id):
    """ Смена пароля """
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({**form.errors, **{'success': False}})


@csrf_protect
@login_required
def account_change_email(request, language, id, step):
    """ Смена email """
    if step == 1:
        form = AccountChangeEmailForm(request, {'username': request.user.username,
                                                'password': request.POST.get('password'),
                                                'new_email': request.POST.get('new_email')})
        if form.is_valid():
            send_auth_mail(request, 'change-email', request.user, form.cleaned_data['new_email'])
            return JsonResponse({'success': True, 'username': request.user.username})
        else:
            if '__all__' in form.errors.keys():
                t = WrapperTranslations.objects.get(active=True)
                form.errors['password'] = [t.wrong_password]
                del form.errors['__all__']
            return JsonResponse({**form.errors, **{'success': False}})
    elif step == 2:
        response = key_verification(request, language)
        if response['success']:
            user = request.user
            key_model = EmailVerification.objects.get(user=user)
            user.email = key_model.new_email
            user.save()
            key_model.delete()
        return JsonResponse(response)


@csrf_protect
@login_required
def account_change_personal_data(request, language, id):
    """ Смена личных данных """
    form = AccountChangePersonalDataForm(request, {'username': request.user.username,
                                                   'password': request.POST.get('password'),
                                                   'new': request.POST.get('new')})
    if form.is_valid():
        fcd = form.cleaned_data
        profile = Profile.objects.get(user=request.user)
        req = ChangePersonalDataRequest(profile=profile, new=fcd['new'])
        req_type = request.POST.get('type')
        if req_type in ['name', 'surname', 'phone', 'address']:
            req.type = req_type
            req.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        if '__all__' in form.errors.keys():
            t = WrapperTranslations.objects.get(active=True)
            form.errors['password'] = [t.wrong_password]
            del form.errors['__all__']
        return JsonResponse({**form.errors, **{'success': False}})


def is_moderator(user):
    return Profile.objects.get(user=user).is_moderator


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_fix_dishes(request, language, id):
    for menu in Menu.objects.all():
        for day_i, day_dishes in enumerate(
                [menu.day1, menu.day2, menu.day3, menu.day4, menu.day5, menu.day6, menu.day7, menu.day8, menu.day9, menu.day10, menu.day11, menu.day12, menu.day13, menu.day14, menu.day15, menu.day16, menu.day17, menu.day18, menu.day19, menu.day20, menu.day21, menu.day22, menu.day23, menu.day24, menu.day25, menu.day26]):
            all_dishes = \
                [menu.day1_other, menu.day2_other, menu.day3_other, menu.day4_other, menu.day5_other, menu.day6_other, menu.day7_other, menu.day8_other, menu.day9_other, menu.day10_other, menu.day11_other, menu.day12_other, menu.day13_other, menu.day14_other, menu.day15_other, menu.day16_other, menu.day17_other, menu.day18_other, menu.day19_other, menu.day20_other, menu.day21_other, menu.day22_other, menu.day23_other, menu.day24_other, menu.day25_other, menu.day26_other][day_i]
            for dish in day_dishes.all():
                if dish not in all_dishes.all():
                    all_dishes.add(dish)
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_download_reports(request, language, id):
    one_day = False
    if ' — ' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' — ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    elif 'אל' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' אל ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    else:
        day, month, year = request.POST.get('dates').split('.')
        date_from = datetime.date(int(year), int(month), int(day))
        date_to = date_from
        one_day = True
    orders = Order.objects.all()
    for order in orders:
        if order.freezes.filter(finished=False):
            if datetime.date.today() >= order.freezes.get(finished=False).frozen_from:
                orders = orders.exclude(id=order.id)
    output = BytesIO()
    book = Workbook(output, {'in_memory': True})
    sheet_name = f'Заказы {date_from.strftime("%d.%m.%y")} - {date_to.strftime("%d.%m.%y")}'
    if one_day:
        sheet_name = f'Заказы {date_from.strftime("%d.%m.%y")}'
    sheet = book.add_worksheet(sheet_name)
    sheet_data = []
    if orders:
        headers = ['#', 'План', 'Дней', 'Заказчик', 'Телефон', 'Адрес', 'Комментарий', 'С', 'По', 'Цена', 'Обработано', 'Оплата', 'Создано']
        dates_range = [date_from + datetime.timedelta(days=x) for x in range((date_to - date_from).days + 1)]
        for date in dates_range:
            headers.append(date.strftime('%d.%b'))
        sheet_data.append(headers)
        for order in orders:
            order_data = [order.id, order.menu.name, order.days,
                          order.name, order.phone, order.address, order.comment, order.first_date.strftime('%d.%m.%Y'),
                          order.last_date.strftime('%d.%m.%Y'), order.price, ('+' if order.is_completed else '-'),
                          ('+' if order.is_payed else '-'), order.created.strftime('%H:%M:%S %d.%m.%Y')]
            order_dishes_circle = get_order_to_order_dishes_circle(order, False)
            days_circle, last_date = get_days_circle(order, order.days, True)
            locale.setlocale(
                category=locale.LC_ALL,
                locale="ru_RU"
            )
            one_day_have_delivery = True
            have_delivery = 0
            for date in dates_range:
                order_data.append('')
                if date.strftime('%d.%m') in days_circle.keys():
                    frozen_from = False
                    frozen_to = False
                    if order.freezes.filter(finished=False):
                        freeze_last = order.freezes.get(finished=False)
                        frozen_from = freeze_last.frozen_from
                        if freeze_last.frozen_to:
                            if freeze_last.frozen_to <= date:
                                frozen_from = False
                                frozen_to = False
                            else:
                                frozen_to = freeze_last.frozen_to
                    frozen = False
                    if frozen_from:
                        if date >= frozen_from:
                            frozen = True
                            if frozen_to:
                                if date <= frozen_to:
                                    frozen = False
                    if not frozen:
                        day_dishes_names = [dish.name_ru for dish in order_dishes_circle[days_circle[date.strftime('%d.%m')]].all().order_by('type')]
                        order_data[-1] = '\n\r'.join(day_dishes_names)
                    else:
                        order_data[-1] = 'Заморожен'
                    have_delivery += 1
                else:
                    one_day_have_delivery = False
            if one_day:
                if one_day_have_delivery:
                    sheet_data.append(order_data)
            else:
                if have_delivery:
                    sheet_data.append(order_data)
        column_widths = [0] * len(headers)
        cell_format = book.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        for row_i, row in enumerate(sheet_data):
            for col_i, col in enumerate(row):
                sheet.write(row_i, col_i, col, cell_format)
                col_width = (len(str(col)) * 1.2)
                if '\n\r' in str(col):
                    col_parts_max_len = 0
                    for col_part in col.split('\n\r'):
                        col_parts_max_len = max(col_parts_max_len, len(col_part))
                    col_width = col_parts_max_len * 1.2
                column_widths[col_i] = max(col_width, column_widths[col_i])
        for col_i, col_width in enumerate(column_widths):
            sheet.set_column(col_i, col_i, col_width)
        book.close()
        output.seek(0)
        filename = 'report_' + date_from.strftime('%d-%m-%Y') + '_' + date_to.strftime('%d-%m-%Y')
        if one_day:
            filename = 'report_' + date_from.strftime('%d-%m-%Y')
        response = HttpResponse(output.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        output.close()
        return response
    else:
        return HttpResponse('За данный период нет отчётов.')


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_download_reports_dishes(request, language, id):
    one_day = False
    if ' — ' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' — ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    elif 'אל' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' אל ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    else:
        day, month, year = request.POST.get('dates').split('.')
        date_from = datetime.date(int(year), int(month), int(day))
        date_to = date_from
        one_day = True
    output = BytesIO()
    book = Workbook(output, {'in_memory': True})
    sheet_name = f'Блюда {date_from.strftime("%d.%m.%y")} - {date_to.strftime("%d.%m.%y")}'
    if one_day:
        sheet_name = f'Блюда {date_from.strftime("%d.%m.%y")}'
    sheet = book.add_worksheet(sheet_name)
    dates_range = [date_from + datetime.timedelta(days=x) for x in range((date_to - date_from).days + 1)]
    headers = ['Блюдо', 'План питания', 'Количество', 'Всего']
    cell_format = book.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format_border = book.add_format()
    cell_format_border.set_text_wrap()
    cell_format_border.set_align('center')
    cell_format_border.set_align('vcenter')
    cell_format_border.set_border()
    cell_format_border_bottom = book.add_format()
    cell_format_border_bottom.set_text_wrap()
    cell_format_border_bottom.set_align('center')
    cell_format_border_bottom.set_align('vcenter')
    cell_format_border_bottom.set_top()
    cell_format_border_bottom.set_left()
    cell_format_border_bottom.set_right()
    cell_format_border_bottom.set_bottom(2)
    cell_format_border_bottom_right = book.add_format()
    cell_format_border_bottom_right.set_text_wrap()
    cell_format_border_bottom_right.set_align('center')
    cell_format_border_bottom_right.set_align('vcenter')
    cell_format_border_bottom_right.set_top()
    cell_format_border_bottom_right.set_left()
    cell_format_border_bottom_right.set_right(2)
    cell_format_border_bottom_right.set_bottom(2)
    cell_format_bold = book.add_format()
    cell_format_bold.set_text_wrap()
    cell_format_bold.set_align('center')
    cell_format_bold.set_align('vcenter')
    cell_format_bold.set_bold()
    cell_format_bold.set_border()

    sheet.merge_range(0, 0, 0, 3, sheet_name, cell_format_border_bottom)
    for i, header in enumerate(headers):
        sheet.write(1, i, header, cell_format_border_bottom)
    dish_count = {}
    orders = Order.objects.filter(is_completed=True)
    for order in orders:
        order_dishes_circle = get_order_to_order_dishes_circle(order, False)
        days_circle, last_date = get_days_circle(order, order.days, True)
        for date in dates_range:
            if date.strftime('%d.%m') in days_circle.keys():
                frozen_from = False
                frozen_to = False
                if order.freezes.filter(finished=False):
                    freeze_last = order.freezes.get(finished=False)
                    frozen_from = freeze_last.frozen_from
                    if freeze_last.frozen_to:
                        if freeze_last.frozen_to <= date:
                            frozen_from = False
                            frozen_to = False
                        else:
                            frozen_to = freeze_last.frozen_to
                frozen = False
                if frozen_from:
                    if date >= frozen_from:
                        frozen = True
                        if frozen_to:
                            if date <= frozen_to:
                                frozen = False
                if not frozen:
                    for dish in order_dishes_circle[days_circle[date.strftime('%d.%m')]].all().order_by('type'):
                        if dish.name_ru not in dish_count.keys():
                            dish_count[dish.name_ru] = {
                                'all': 0,
                                'menus': {}
                            }
                        dish_count[dish.name_ru]['all'] += 1
                        menu_name = order.menu.name
                        if menu_name not in dish_count[dish.name_ru]['menus'].keys():
                            dish_count[dish.name_ru]['menus'][menu_name] = 0
                        dish_count[dish.name_ru]['menus'][menu_name] += 1
    row_i = 2
    column_widths = [len(header) * 1.2 for header in headers]
    for dish_name, dish_data in dish_count.items():
        row_i_start = row_i
        menus_counter = 1
        for menu_name, menu_count in dish_data['menus'].items():
            if menus_counter == len(dish_data['menus'].items()):
                sheet.write(row_i, 1, menu_name, cell_format_border_bottom)
                sheet.write(row_i, 2, menu_count, cell_format_border_bottom)
            else:
                sheet.write(row_i, 1, menu_name, cell_format_border)
                sheet.write(row_i, 2, menu_count, cell_format_border)
            menus_counter += 1
            if len(menu_name) * 1.2 > column_widths[1]:
                column_widths[1] = len(menu_name) * 1.2
            if len(str(menu_count)) * 1.2 > column_widths[2]:
                column_widths[2] = len(str(menu_count)) * 1.2
            row_i += 1
        if row_i-1 - row_i_start == 0:
            sheet.write(row_i_start, 0, dish_name, cell_format_border_bottom_right)
            sheet.write(row_i_start, 3, dish_data['all'], cell_format_border_bottom_right)
        else:
            sheet.merge_range(row_i_start, 0, row_i-1, 0, dish_name, cell_format_border_bottom_right)
            sheet.merge_range(row_i_start, 3, row_i-1, 3, dish_data['all'], cell_format_border_bottom_right)
        if len(dish_name) * 1.2 > column_widths[0]:
            column_widths[0] = len(dish_name) * 1.2
        if len(str(dish_data['all'])) * 1.2 > column_widths[3]:
            column_widths[3] = len(str(dish_data['all'])) * 1.2
    for col_i, col_width in enumerate(column_widths):
        sheet.set_column(col_i, col_i, col_width)
    book.close()
    output.seek(0)
    filename = 'dishes_' + date_from.strftime('%d-%m-%Y') + '_' + date_to.strftime('%d-%m-%Y')
    if one_day:
        filename = 'dishes_' + date_from.strftime('%d-%m-%Y')
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
    output.close()
    return response


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_download_reports_delivery(request, language, id):
    one_day = False
    if ' — ' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' — ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    elif 'אל' in request.POST.get('dates'):
        date_from_str, date_to_str = request.POST.get('dates').split(' אל ')
        date_from_splt = date_from_str.split('.')
        date_to_splt = date_to_str.split('.')
        date_from = datetime.date(int(date_from_splt[2]), int(date_from_splt[1]), int(date_from_splt[0]))
        date_to = datetime.date(int(date_to_splt[2]), int(date_to_splt[1]), int(date_to_splt[0]))
    else:
        day, month, year = request.POST.get('dates').split('.')
        date_from = datetime.date(int(year), int(month), int(day))
        date_to = date_from
        one_day = True
    output = BytesIO()
    book = Workbook(output, {'in_memory': True})
    sheet_name = f'{date_from.strftime("%d.%m.%y")} - {date_to.strftime("%d.%m.%y")}'
    if one_day:
        sheet_name = f'{date_from.strftime("%d.%m.%y")}'
    sheet = book.add_worksheet(sheet_name)
    dates_range = [date_from + datetime.timedelta(days=x) for x in range((date_to - date_from).days + 1)]
    headers = ['#', 'Заказчик', 'Телефон', 'Адрес', 'Комментарий', 'Цена']
    cell_format = book.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_border()
    cell_format_no_border = book.add_format()
    cell_format_no_border.set_text_wrap()
    cell_format_no_border.set_align('center')
    cell_format_no_border.set_align('vcenter')
    cell_format_bold = book.add_format()
    cell_format_bold.set_text_wrap()
    cell_format_bold.set_align('center')
    cell_format_bold.set_align('vcenter')
    cell_format_bold.set_bold()
    cell_format_bold.set_border()
    column_widths = [len(header) * 1.2 for header in headers]
    row_i = 0
    if one_day:
        sheet.merge_range(row_i, 0, row_i, 5, date_from.strftime('%d.%m.%Y'), cell_format_no_border)
    else:
        sheet.merge_range(row_i, 0, row_i, 5, date_from.strftime('%d.%m.%Y') + ' - ' + date_to.strftime('%d.%m.%Y'), cell_format_no_border)
    row_i += 1
    for i, header in enumerate(headers):
        sheet.write(row_i , i, header, cell_format_bold)
    row_i += 1
    ready_orders = []
    orders = Order.objects.filter(is_completed=True)
    for order in orders:
        days_circle, last_date = get_days_circle(order, order.days, True)
        not_found_date = True
        dates_range_i = 0
        while not_found_date:
            date = dates_range[dates_range_i]
            if date.strftime('%d.%m') in days_circle.keys():
                frozen_from = False
                frozen_to = False
                if order.freezes.filter(finished=False):
                    freeze_last = order.freezes.get(finished=False)
                    frozen_from = freeze_last.frozen_from
                    if freeze_last.frozen_to:
                        if freeze_last.frozen_to <= date:
                            frozen_from = False
                            frozen_to = False
                        else:
                            frozen_to = freeze_last.frozen_to
                frozen = False
                if frozen_from:
                    if date >= frozen_from:
                        frozen = True
                        if frozen_to:
                            if date <= frozen_to:
                                frozen = False
                if not frozen:
                    if order not in ready_orders:
                        ready_orders.append(order)
                    not_found_date = False
            if dates_range_i + 1 == len(dates_range):
                not_found_date = False
            if not_found_date:
                dates_range_i += 1
    for order in ready_orders:
        sheet.write(row_i, 0, order.id, cell_format)
        if len(str(order.id)) * 1.2 > column_widths[0]:
            column_widths[0] = len(str(order.id)) * 1.2
        sheet.write(row_i, 1, order.name, cell_format)
        if order.name:
            if len(order.name) * 1.2 > column_widths[1]:
                column_widths[1] = len(order.name) * 1.2
        sheet.write(row_i, 2, order.phone, cell_format)
        if order.phone:
            if len(order.phone) * 1.2 > column_widths[2]:
                column_widths[2] = len(order.phone) * 1.2
        sheet.write(row_i, 3, order.address, cell_format)
        if order.address:
            if len(order.address) * 1.2 > column_widths[3]:
                column_widths[3] = len(order.address) * 1.2
        sheet.write(row_i, 4, order.comment, cell_format)
        if order.comment:
            if len(order.comment) * 1.2 > column_widths[4]:
                column_widths[4] = len(order.comment) * 1.2
        if not order.is_payed:
            sheet.write(row_i, 5, order.price, cell_format)
            if len(str(order.price)) * 1.2 > column_widths[5]:
                column_widths[5] = len(str(order.price)) * 1.2
        else:
            sheet.write(row_i, 5, '', cell_format)
        row_i += 1
    for col_i, col_width in enumerate(column_widths):
        sheet.set_column(col_i, col_i, col_width)
    book.close()
    output.seek(0)
    filename = 'delivery_' + date_from.strftime('%d-%m-%Y') + '_' + date_to.strftime('%d-%m-%Y')
    if one_day:
        filename = 'delivery_' + date_from.strftime('%d-%m-%Y')
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
    output.close()
    return response


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_download_reports_orders(request, language, id):
    day, month, year = request.POST.get('date').split('.')
    date = datetime.date(int(year), int(month), int(day))
    orders = []
    for order in Order.objects.filter(is_completed=True).order_by('-created'):
        translation.activate('ru')
        order_data = {
            'ru': {
                'id': order.id,
                'menu': order.menu.name,
                'description': order.menu.description,
                'dishes': [],
            },
        }
        translation.activate('he')
        order_data['he'] = {
            'id': order.id,
            'menu': order.menu.name,
            'description': order.menu.description,
            'dishes': [],
        }
        order_dishes_circle = get_order_to_order_dishes_circle(order, False)
        days_circle, last_date = get_days_circle(order, order.days, True)
        summary = {'calories': 0, 'proteins': 0, 'fats': 0, 'carbohydrates': 0}
        daytime_order = [
            'drink',
            'breakfast',
            'second-breakfast',
            'lunch',
            'high-tea',
            'dinner',
        ]
        order_dishes_circle = get_order_to_order_dishes_circle(order, False)
        days_circle, last_date = get_days_circle(order, order.days, True)
        if date.strftime('%d.%m') in days_circle.keys():
            frozen_from = False
            frozen_to = False
            if order.freezes.filter(finished=False):
                freeze_last = order.freezes.get(finished=False)
                frozen_from = freeze_last.frozen_from
                if freeze_last.frozen_to:
                    if freeze_last.frozen_to <= date:
                        frozen_from = False
                        frozen_to = False
                    else:
                        frozen_to = freeze_last.frozen_to
            frozen = False
            if frozen_from:
                if date >= frozen_from:
                    frozen = True
                    if frozen_to:
                        if date <= frozen_to:
                            frozen = False
            if not frozen:
                for daytime in daytime_order:
                    for dish in order_dishes_circle[days_circle[date.strftime('%d.%m')]].filter(type=daytime):
                        translation.activate('ru')
                        order_data['ru']['dishes'].append({
                            'name': dish.name,
                            'description': dish.description,
                            'calories': dish.calories,
                            'proteins': dish.proteins,
                            'fats': dish.fats,
                            'carbohydrates': dish.carbohydrates,
                        })
                        translation.activate('he')
                        order_data['he']['dishes'].append({
                            'name': dish.name,
                            'description': dish.description,
                            'calories': dish.calories,
                            'proteins': dish.proteins,
                            'fats': dish.fats,
                            'carbohydrates': dish.carbohydrates,
                        })
                        summary['calories'] = summary['calories'] + dish.calories
                        summary['proteins'] = summary['proteins'] + dish.proteins
                        summary['fats'] = summary['fats'] + dish.fats
                        summary['carbohydrates'] = summary['carbohydrates'] + dish.carbohydrates
                order_data['ru']['summary'] = summary
                order_data['he']['summary'] = summary
                orders.append(order_data)
    context = {'fixed': Fixed.objects.get(active=True), 'orders': orders}
    html_content = get_template('reports-orders.html').render(context)
    response = HttpResponse(html_content)
    return response


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_make_order_payed(request, language, id):
    Order.objects.filter(id=request.POST['order_id']).update(is_payed=True)
    return JsonResponse({
        'success': True,
        'order': generate_orders_json(Order.objects.filter(id=request.POST['order_id']), True)['orders'][0],
        'today': datetime.date.today().strftime('%e.%m.%Y')
    })


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_make_order_to_return_payed(request, language, id):
    Order.objects.filter(id=request.POST['order_id']).update(to_return=0)
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_change_request_delete(request, language, id):
    """ Модерация: отклонить смену личных данных """
    ChangePersonalDataRequest.objects.get(id=request.POST['change_id']).delete()
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_change_request_exec(request, language, id):
    """ Модерация: принять смену личных данных """
    for req in ChangePersonalDataRequest.objects.filter(id=request.POST['change_id']):
        req.done = True
        req.save()
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_order_complete_delete(request, language, id):
    """ Модерация: отклонить заказ по телефону """
    Order.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_order_complete_submit(request, language, id):
    """ Модерация: принять заказ """
    order = Order.objects.filter(id=request.POST.get('id'))
    print(order[0].referral_id)
    form = OrderCallForm(request.POST)
    if form.is_valid():
        fcd = form.cleaned_data
        order.update(name=fcd['name'], email=fcd['email'], address=fcd['address'], comment=fcd['comment'],
                     is_completed=True)
        # send payment mail/sms
        order = order[0]
        send_new_order_messages(order, True)
        if order.referral_id:
            print(1)
            if Profile.objects.filter(id=order.referral_id):
                print(2)
                profile = Profile.objects.get(id=order.referral_id)
                promocode = PromoCode.objects.create(profile=profile)
                send_whatsapp_message('client_receive_promocode', profile.phone, promocode)
                if order.profile.referral_id:
                    order.profile.referral_id = None
                    order.profile.save()
        return JsonResponse({'success': True, 'order_id': order.id})
    else:
        return JsonResponse({**form.errors, **{'success': False}})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_call_request_load_price(request, language, id):
    """ Модерация: Загрузить цену """
    menu = Menu.objects.get(type=request.POST.get('menu'))
    days = int(request.POST.get('days'))
    day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
    first_date_delay = 1
    first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(
        days=first_date_delay)
    if request.POST.get('first_date'):
        day, month, year = request.POST.get('first_date').split('.')
        first_date = datetime.date(int(year), int(month), int(day))
    days_to_price = get_menu_days_to_price(menu)
    home_settings = HomePageSettings.objects.get(active=True)
    price = Decimal(days_to_price[days])
    return JsonResponse({'success': True, 'price': price})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_call_request_delete(request, language, id):
    """ Модерация: отклонить заказ через звонок """
    CallRequest.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_call_request_submit(request, language, id):
    """ Модерация: создать заказ через звонок """
    form = OrderForm(request.POST)
    if form.is_valid():
        fcd = form.cleaned_data
        phone = fcd['phone']
        email = fcd['email']
        address = fcd['address']
        payment_type = fcd['payment_type']
        referral_id = fcd['referral_id']
        name = request.POST.get('name')
        days = int(request.POST.get('days'))
        menu = Menu.objects.get(active=True, id=request.POST.get('menu_id'))
        day, month, year = timezone.localtime().strftime('%e-%m-%Y').split('-')
        first_date_delay = 1
        first_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(
            days=first_date_delay)
        if request.POST.get('first_date'):
            day, month, year = request.POST.get('first_date').split('.')
            first_date = datetime.date(int(year), int(month), int(day))
        new_order = Order(
            menu=menu,
            first_date=first_date,
            days=days,
            payment_type=payment_type,
            phone=phone,
            name=name,
            email=email,
            address=address,
            is_completed=True
        )
        if referral_id:
            new_order.referral_id = referral_id
        new_order = new_order.save()['order']
        send_new_order_messages(new_order, True)
        if new_order.referral_id:
            if Profile.objects.filter(id=new_order.referral_id):
                profile = Profile.objects.get(id=new_order.referral_id)
                promocode = PromoCode.objects.create(profile=profile)
                send_whatsapp_message('client_receive_promocode', profile.phone, promocode)
        # send payment mail/sms
        CallRequest.objects.get(id=request.POST.get('id')).delete()
        return JsonResponse({'success': True, 'id': new_order.id})
    else:
        return JsonResponse({**form.errors, **{'success': False}})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_review_request_delete(request, language, id):
    """ Модерация: отклонить отзыв """
    Review.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse({'success': True})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_review_request_submit(request, language, id):
    """ Модерация: принять отзыв """
    form = ReviewForm(request.POST, request.FILES)
    if form.is_valid():
        review = form.save()
        review.is_moderated = True
        review.save()
        Review.objects.get(id=request.POST['id']).delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({**form.errors, **{'success': False}})


@csrf_protect
@login_required
@user_passes_test(is_moderator)
def moderator_account_download_backup(request, language, id):
    return FileResponse(open(os.path.join(f'/home/{settings.LINUX_USER}/backups/backup.tar.gz'), 'rb'))
