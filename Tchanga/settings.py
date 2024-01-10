"""
Django settings for Tchanga project.

Generated by 'django-admin startproject' using Django 3.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from tzlocal import get_localzone
import dj_database_url
from urllib.parse import urlparse , urlencode, parse_qs



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY ='bfb6c1140d595eaf0fc50054b03d7c0d'#parse_qs(os.environ.get('SECRET_KEY'))#'django-insecure-ph+676$%oyyv73(vr#!q-s@t_p6rhow8$6$rg_&*7@09+_%jy1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =os.environ.get("DEBUG",False)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","127.0.0.1 ").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plan',
    'users',
    'kasse'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'Tchanga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION='Tchanga.wsgi.application'

#WSGI_APPLICATION = 'Tchanga.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':BASE_DIR / 'db.sqlite3'  #'/home/alassane/Desktop/Dev-Projects/PythonProjects/Django/tchanga/db.sqlite3',    #BASE_DIR / 'db.sqlite3',
    }
}

parsed_url=parse_qs(os.environ.get("DATABASE_URL"))
durl=os.environ.get("DATABASE_URL")
DATABASES['default']=parsed_url #parsed_url  os.environ.get("DATABASE_URL") 'postgres://tchangabase_user:qQ0UnP8IY5XcE9kPXmmlE9648GLAXWLc@dpg-cmdlpf8cmk4c73alkbpg-a.frankfurt-postgres.render.com/tchangabase'  dj_database_url.parse(durl)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
tmz=get_localzone()
TIME_ZONE = str(tmz)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
if not DEBUG:
  STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'plan/static'),
    os.path.join(BASE_DIR,'kasse/static'),
    os.path.join(BASE_DIR,'users/static')
                  ]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
