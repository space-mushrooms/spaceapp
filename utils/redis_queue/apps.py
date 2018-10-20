from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class RedusQueueAppConfig(AppConfig):
    name = 'utils.redis_queue'
    verbose_name = 'RedisQueue'

    def ready(self):
        autodiscover_modules('tasks')
