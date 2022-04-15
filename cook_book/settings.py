import os
from pathlib import Path

import cloudinary
from django.conf.global_settings import SESSION_EXPIRE_AT_BROWSER_CLOSE
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(' ')
APP_ENV = os.getenv('APP_ENV')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

COOK_BOOK_APPS = [
    'cook_book.cook_book_auth',
    'cook_book.cook_book_profiles',
    'cook_book.cook_book_main_app',
    'cloudinary',
]

THIRD_PARTY_APPS = []

INSTALLED_APPS = DJANGO_APPS + COOK_BOOK_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'cook_book.cook_book_main_app.middlewares.handle_exception',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cook_book.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cook_book.wsgi.application'

DATABASES = None

if APP_ENV == 'Production':
    DATABASES = {
        'default': {
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cook_book_db',
            'USER': 'postgres',
            'PASSWORD': 'maria19',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'cook_book.cook_book_auth.validators.MinimumLengthValidatorCustom',
    },
    {
        'NAME': 'cook_book.cook_book_auth.validators.NumericPasswordValidatorCustom',
    },
    {
        'NAME': 'cook_book.cook_book_auth.validators.CommonPasswordValidatorCustom',
    },
]

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
STATICFILES_DIRS = BASE_DIR / 'static',
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media_files'

LOGIN_URL = reverse_lazy('sign in')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'cook_book_auth.CookBookCustomUser'


EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
