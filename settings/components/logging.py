import os

from settings import BASE_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'tasks': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'tasks.log'),
            'maxBytes': 1024 * 1024 * 30,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'rq_console': {
            'level': 'DEBUG',
            'class': 'rq.utils.ColorizingStreamHandler',
            'formatter': 'rq_console',
            'exclude': ['%(asctime)s'],
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'debug': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apps': {
            'handlers': ['sentry', 'tasks'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tools_project': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'haystack': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'rq.worker': {
            'handlers': ['rq_console', 'sentry', 'tasks'],
            'level': 'DEBUG'
        },
        'backoff': {
            'level': 'WARN',
        },
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}
