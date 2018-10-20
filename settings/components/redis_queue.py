from settings import REDIS_HOST, REDIS_DB

RQ_QUEUE_DEFAULT = 'default'
RQ_QUEUE_NOTIFICATIONS = 'notifications'


def get_connection(**kwargs):
    _RQ_DEFAULT_CONNECTION = {
        'HOST': REDIS_HOST,
        'PORT': 6379,
        'DB': REDIS_DB.get('tasks'),
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
    _RQ_DEFAULT_CONNECTION.update(kwargs)
    return _RQ_DEFAULT_CONNECTION


RQ_QUEUES = {
    RQ_QUEUE_DEFAULT: get_connection(),
    RQ_QUEUE_NOTIFICATIONS: get_connection(),
}

RQ_SHOW_ADMIN_LINK = False  # show rq in admin, rq admin will be available on direct link, see crm/urls.py
RQ_SYNC_MODE = False  # run task in sync mode (useful for tests or local development)
