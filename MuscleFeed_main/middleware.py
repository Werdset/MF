import pytz
from django.shortcuts import redirect
from django.utils import timezone, translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import LANGUAGE_SESSION_KEY

from MuscleFeed_settings import settings
from .models import Profile
from .views import activate_translations


class LocalizationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        request_path = request.path.split('/')
        if len(request_path) > 2:
            if settings.LOCAL:
                if request_path[1] in [settings.STATIC_URL.replace('/', ''), settings.MEDIA_URL.replace('/', '')]:
                    if settings.LANGUAGE_COOKIE_NAME in request.session.keys():
                        activate_translations(request, request.session[settings.LANGUAGE_COOKIE_NAME])
                    return self.get_response(request)
            if request_path[1] in ['admin']:
                if settings.LANGUAGE_COOKIE_NAME in request.session.keys():
                    request.session[LANGUAGE_SESSION_KEY] = 'ru'
                    activate_translations(request, 'ru')
                return self.get_response(request)
            languages = ['ru', 'he']
            if request_path[1] in languages:
                activate_translations(request, request_path[1])
                return self.get_response(request)
            else:
                activate_translations(request, 'he')
                return redirect('home', 'he')
        else:
            if settings.LANGUAGE_COOKIE_NAME in request.session.keys():
                activate_translations(request, request.session[settings.LANGUAGE_COOKIE_NAME])
            return self.get_response(request)

