"""
Django settings for the project.

Generated by 'django-admin startproject' using Django 2.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tjb5r66hgdjd@-p1ay0fz%+vamycfs66#y910+tb^xp=6+yx_+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*',]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:9000",
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000']
CORS_ALLOW_CREDENTIALS = True

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'django_celery_results'
]

LOCAL_APPS = [
    'apps.core',
]

INSTALLED_APPS = THIRD_PARTY_APPS + LOCAL_APPS + DJANGO_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# AUTH_USER_MODEL = 'seguridad.Usuario'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = False

USE_TZ = False

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
SITE_URL = "http://127.0.0.1:8000/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATIC_URL = f'{SITE_URL}public/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = f'{SITE_URL}media/'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.SizedPageNumberPagination',
    'PAGE_SIZE': None
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.seguridad.jwt_utils.jwt_response_payload_handler',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'contactabilidad',
        'USER': 'contactabilidad',
        'PASSWORD': 'contactabilidad',
        'HOST': 'dev-contactabilidad-db',
        'PORT': '5432',
    }
}

FILE_URL = '/Users/iid/dev/ALCALDIA-MEDELLIN/framework-scraping/backend/config/media/'

MEDIA_URL = '/media/'
STATIC_URL = '/public/'

FORMATO_FECHA = "%Y-%m-%d %H:%M"

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://dev-contactabilidad-redis:6379/0'
CELERY_TIMEZONE = 'America/Bogota'

EXCEL_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
