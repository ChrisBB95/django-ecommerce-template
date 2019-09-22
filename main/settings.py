import os
import socket
import paypalrestsdk

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dev_hosts = ['Tim','DESKTOP-RM34RT3']

if socket.gethostname() in dev_hosts:
    from main.local_settings import *
    SECRET_KEY = '###################################'
else:
    with open('/var/www/auth/key.txt', 'r') as f:
        import pymysql
        from main.production_settings import *
        SECRET_KEY = f.read().strip()
        pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = ['bucketmeadow.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #own apps
    'home',
    'payment',
    'shop',
]

#Payment API Keys
PAYMENT_LIVE = False
if socket.gethostname() == 'Tim' or not PAYMENT_LIVE:
    STRIPE_PUBLIC_KEY = "######"    #TEST KEY
    STRIPE_SECRET_KEY = "######"    #TEST KEY
    paypalrestsdk.configure({
        'mode': 'sandbox',
        'client_id': '######',      #TEST KEY
        'client_secret': '######',  #TEST KEY
    })
else:
    STRIPE_PUBLIC_KEY = "######"    #PRODUCTION KEY
    STRIPE_SECRET_KEY = "######"    #PRODUCTION KEY
    paypalrestsdk.configure({
        'mode': 'live',
        'client_id': '######',      #PRODUCTION KEY
        'client_secret': '######'   #PRODUCTION KEY
    })

#Email Service Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '###'
EMAIL_HOST_USER = '###'
DEFAULT_FROM_EMAIL = '###'
SERVER_EMAIL = '###'
EMAIL_HOST_PASSWORD = '###'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

ROOT_URLCONF = 'main.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Anchorage'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [(os.path.join(BASE_DIR, "static"))]

if socket.gethostname() in dev_hosts:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    STATIC_ROOT = '/var/www/public/static'
    MEDIA_ROOT = '/var/www/public/media'
