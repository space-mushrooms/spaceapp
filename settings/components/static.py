import os

from settings import BASE_DIR

STATIC_URL = '/st/'
STATIC_ROOT = os.path.join(BASE_DIR, 'st')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMP_ROOT = os.path.join(BASE_DIR, 'tmp')
