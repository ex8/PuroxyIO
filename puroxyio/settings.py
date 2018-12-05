import json
import os
from django.contrib.messages import constants as messages
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(file='{}/puroxyio/settings.json'.format(BASE_DIR), encoding='utf8') as f:
    configuration = json.loads(f.read())

SECRET_KEY = configuration["SECRET_KEY"]

DEBUG = False
ORDER = True

ALLOWED_HOSTS = [
    'puroxy.io',
    'www.puroxy.io',
    'localhost'
]

INSTALLED_APPS = [
    'main',
    'blog',
    'interface',
    'products',
    'orders',
    'invoices',
    'services',
    'payments',
    'tickets',
    'api',
    'rest_framework',
    'admin_honeypot',
    'django_crontab',
    'ckeditor',
    'snowpenguin.django.recaptcha2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication backends for auth views
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'interface.authentication.EmailAuthBackend',
)

# Routes configuration
ROOT_URLCONF = 'puroxyio.urls'
LOGIN_REDIRECT_URL = reverse_lazy('interface:dashboard')
LOGIN_URL = reverse_lazy('interface:login')
LOGOUT_URL = reverse_lazy('interface:logout')

# Template and views engine
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

# Cronjob configuration
CRONJOBS = [
    ('0 7 * * *', 'invoices.cron.invoice_cron')
]

# RESTful API configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/day',
        'user': '200/day'
    }
}

# SparkPost Email Configuration
EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'
SPARKPOST_API_KEY = configuration["SPARKPOST_API_KEY"]
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# WSGI container
WSGI_APPLICATION = 'puroxyio.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'puroxyio',
        'USER': 'puroxyio_user',
        'PASSWORD': configuration["DATABASE_PASSWORD"],
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validators
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

# Date & time configuration
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Cookie session age; 3600 (1 hour) before destroying
# Session Cookie Secure; send cookies over HTTPS ONLY
# CSRF_COOKIE_SECUURE; send csrf token cookies over HTTPS ONLY
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Static folder configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Web hosting configuration
WEB_HOST_MAIN_IP = configuration['WEB_HOST_MAIN_IP']
WEB_HOST_OPERATING_SYSTEM = 'CloudLinux 6.6 64-bit'
WEB_HOST_BASE_URL = configuration["WEB_HOST_BASE_URL"]
WEB_HOST_USERNAME = 'root'
WEB_HOST_PASSWORD = configuration["WEB_HOST_PASSWORD"]
WEB_HOST_CONTROL_PANEL = 'cPanel'

# SolusVM URL for API requests
SOLUSVM_URL = configuration["SOLUSVM_URL"]

# Payments configuration
COINPAYMENTS_MERCHANT_ID = configuration["COINPAYMENTS_MERCHANT_ID"]
COINPAYMENTS_IPN_SECRET = configuration["COINPAYMENTS_IPN_SECRET"]

# Google re-captcha
RECAPTCHA_PUBLIC_KEY = configuration["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = configuration["RECAPTCHA_PRIVATE_KEY"]

# Social
TWITTER = 'https://twitter.com/PuroxyIO'
FACEBOOK = 'https://www.facebook.com/PuroxyII'

# Message tag styles
MESSAGE_TAGS = {
    messages.SUCCESS: 'green',
    messages.ERROR: 'red',
    messages.INFO: 'blue',
    messages.WARNING: 'yellow',
}
