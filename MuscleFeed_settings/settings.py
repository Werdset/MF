import datetime
import os
from decimal import Decimal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LINUX_USER = 'mf'

DEBUG = True
LOCAL = True
print(str(Path(__file__).resolve().parent).split('/')[-2])
if os.path.exists(f'/home/{LINUX_USER}/secretkey.txt') and str(Path(__file__).resolve().parent).split('/')[-2] != 'MuscleFeed_dev':
    LOCAL = False


if LOCAL:
    SECRET_KEY = 'blahblahblah'
    PAYMENT_ID = '3689f66e-b858-4356-85a6-ee06ab0c637e'
    PAYMENT_SECRET = 'op5kaf52A8MTexXD6ZH1Qw'
    ALLOWED_HOSTS = ['*']
else:
    with open(f'/home/{LINUX_USER}/secretkey.txt') as f:
        SECRET_KEY = f.read().strip()
    with open(f'/home/{LINUX_USER}/paymentid.txt') as f:
        PAYMENT_ID = f.read().strip()
    with open(f'/home/{LINUX_USER}/paymentsecret.txt') as f:
        PAYMENT_SECRET = f.read().strip()
    ALLOWED_HOSTS = ['206.54.190.158', 'muscle-feed.co.il', 'www.muscle-feed.co.il']

SITE_ID = 1

INSTALLED_APPS = [
    # Real apps
    'MuscleFeed_main.apps.MuscleFeedMainConfig',
    # Plugins apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'ckeditor',
    'modeltranslation',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'MuscleFeed_main.middleware.LocalizationMiddleware',
]

ROOT_URLCONF = 'MuscleFeed_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'MuscleFeed_settings.wsgi.application'

if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_db',
            'USER' : 'django_user',
            'PASSWORD' : '7Kfzva3EW11u0AO6lY',
            'HOST' : '127.0.0.1',
            'PORT' : '5432',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Israel'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('ru', 'Русский'),
    ('he', 'עִברִית'),
]
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'
MODELTRANSLATION_AUTO_POPULATE = True
MODELTRANSLATION_DEBUG = True
LANGUAGE_COOKIE_NAME = 'language'

STATIC_URL = '/files/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
if LOCAL:
    STATICFILES_DIRS = [
       os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/pics/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL = '/#login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_LOCALTIME = True
# mrelay230@gmail.com
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'slotindima@gmail.com'
#EMAIL_HOST_PASSWORD = 'bbnspatzelotizat'

FIRST_GLOBAL_DATE = datetime.date(2020, 9, 28)

CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "stylesheetparser",
        'allowedContent': True,
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-',
             'RemoveFormat'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'sourcearea', 'SpecialChar'],
            ['Link', 'Unlink', 'Anchor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language'],
            ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Find', 'Replace', '-', 'SelectAll', '-', 'Scayt'],
            ['Maximize', 'ShowBlocks']
        ],
    }
}

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': './debug.log',
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#    },
#}
