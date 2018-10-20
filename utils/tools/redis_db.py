import pickle

from redis import StrictRedis

from django.conf import settings

from utils.tools.cached_function import CachedFunction


class PickledRedis(StrictRedis):
    def __init__(self, host=settings.REDIS_HOST, port=6379, db=0, **kwargs):
        # db must be specified
        if db is None:
            raise ValueError('Redis db must be specified')
        super().__init__(host=host, port=port, db=db, **kwargs)

    def get_key(self, name):
        pickled_value = super().get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def get_list(self, keys):
        if not keys:
            return []
        pickled_list = super().mget(keys)
        if pickled_list is None:
            return None
        return [pickle.loads(l) if l else l for l in pickled_list]

    def get(self, name):
        if isinstance(name, (list, tuple)):
            return self.get_list(name)
        return self.get_key(name)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super().set(name, pickle.dumps(value), ex, px, nx, xx)

    def setex(self, name, time, value):
        return super().setex(name, time, pickle.dumps(value))

    @CachedFunction(timeout=100)
    def cached_get(self, name):
        return self.get(name)
