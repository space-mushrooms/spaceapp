import settings
import functools

from django.conf import settings
from redis import StrictRedis

redis = StrictRedis(host=settings.REDIS_HOST)


def single_instance_task(timeout, name=None):
    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if name is None and 'task_postfix' not in kwargs:
                raise ValueError('Name must be defined')

            lock = 'single-instance-task-{}-{}'.format(func.__name__, name or kwargs.pop('task_postfix'))
            is_locked = lambda: redis.exists(lock)
            acquire_lock = lambda: redis.setex(lock, timeout, 'true') if not is_locked() else False
            release_lock = lambda: redis.delete(lock)

            if acquire_lock():
                try:
                    return func(*args, **kwargs)
                finally:
                    release_lock()

        return wrapper

    return dec


def run_if_true(setting):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if setting:
                return func(*args, **kwargs)

        return wrapper

    return decorator
