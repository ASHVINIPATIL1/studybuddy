"""
Django settings for core project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Security
# --------------------------------------------------

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-fallback-key'
)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')


# --------------------------------------------------
# Application definition
# --------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'users',
    'materials',
    'quiz',
    'progress',
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


# --------------------------------------------------
# Templates
# --------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'core.wsgi.application'


# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------------
# Password validation
# --------------------------------------------------

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


# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# File upload limits
# --------------------------------------------------

DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024


# --------------------------------------------------
# Static files
# --------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# --------------------------------------------------
# Media files
# --------------------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------
# Authentication
# --------------------------------------------------

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/users/login/'


# --------------------------------------------------
# API Keys
# --------------------------------------------------

GROQ_API_KEY = os.getenv('GROQ_API_KEY')


# --------------------------------------------------
# Default primary key
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'