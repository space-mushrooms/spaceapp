# -*- coding: utf-8 -*-
from settings import *

ALLOWED_HOSTS = [u'localhost', u'127.0.0.1']

SITE_HOST = 'http://localhost:8000'

DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spaceapp',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',  # Set to empty string for localhost.
        'PORT': '',  # Set to empty string for default.
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 100000000

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

VERSION_STAMP = '1.0.0'
STATIC_URL = '%sv%s/' % (STATIC_URL, VERSION_STAMP.replace(".", ""))

GOOGLE_AUTH = {
    'client_id': '11485322782-ltecers5s2e5a62q1nt9upnfokt967i8.apps.googleusercontent.com',
    'client_secret': '85l3YYL7JAuSkrEMjsagTXOD',
    'redirect_url': 'http://localhost:8080/auth'
}

RAVEN_CONFIG = {
    'dsn': 'http://1bb9e5a48652492fbd80e44fcd12739d:4ece615f92674033a58a7d7ff8589a14@sentry-dev.ostrovok.ru/50',
}
