"""
Django settings for xmppserverui project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1y+xp2ic@04=_t5293l69k%)8c(ika!h3zk&qmqcn9uep088-v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'virtualhost.User'
APPEND_SLASH = True
LOGIN_URL = '/profile/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'virtualhost',
    'server',
    'xmppserverui',

    'xmppserverinstaller',
    'personal_area'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xmppserverui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xmppserverui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'xmppserverui.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Whitenoise
# to serve static from xabber web
WHITENOISE_ROOT = os.path.join(STATIC_ROOT, 'xabberweb')

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Project settings

EJABBERD_API_URL = 'http://127.0.0.1:5280/api'
EJABBERD_API_TOKEN_TTL = 60 * 60 * 24 * 365
EJABBERD_API_SCOPES = 'sasl_auth'

AUTHENTICATION_BACKENDS = [
    'api.backends.EjabberdAPIBackend',
    'api.backends.DjangoUserBackend',
]

UPLOAD_IMG_MAX_SIZE = 10 * 1024 * 1024
GENERATED_PASSWORD_MAX_LEN = 10

PAGINATION_PAGE_SIZE = 30

# in seconds
HTTP_REQUEST_TIMEOUT = 5


# Installer settings

PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
INSTALLATION_LOCK = os.path.join(PROJECT_DIR, '.installation_lock')
PSQL_SCRIPT = os.path.join(PROJECT_DIR, 'psql')
EJABBERD_DUMP = os.path.join(PROJECT_DIR, 'pg.sql')
EJABBERD_CONFIG_PATH = os.path.join(PROJECT_DIR, 'etc/ejabberd/')
EJABBERDCTL = os.path.join(PROJECT_DIR, 'bin/ejabberdctl')
EJABBERD_SHOULD_RELOAD = False
EJABBERD_STATE = os.path.join(PROJECT_DIR, 'server_state')
EJABBERD_STATE_ON = 1
EJABBERD_STATE_OFF = 0

EJABBERD_ADMINS_CONFIG_FILE = 'acl_admin.yml'
EJABBERD_VHOSTS_CONFIG_FILE = 'virtual_hosts.yml'

EJABBERD_EVERYBODY_DEFAULT_GROUP_NAME = "All"
EJABBERD_EVERYBODY_DEFAULT_GROUP_DESCRIPTION = "Contains all users on this virtual host"

PREDEFINED_CONFIG_FILE_PATH = "predefined_config.json"
