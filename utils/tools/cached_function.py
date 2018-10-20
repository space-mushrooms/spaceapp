import functools
import sys
import time


class CachedFunction:
    _caches = {}
    _timeouts = {}
    _last_collect = time.time()

    def __init__(self, timeout=10):
        self.timeout = timeout

    @classmethod
    def collect(cls):
        if 'test' in sys.argv:
            for key in cls._caches:
                cls._caches[key] = {}

        if (time.time() - cls._last_collect) < 10:
            return

        cls._last_collect = time.time()
        for func, func_cache in cls._caches.items():
            cache = {}
            for key, (value, set_time) in func_cache.items():
                if (time.time() - set_time) < cls._timeouts[func]:
                    cache[key] = value, set_time
            cls._caches[func] = cache

    def __call__(self, func):
        self._caches[func] = {}
        self._timeouts[func] = self.timeout

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            self.collect()
            cache = self._caches[func]

            key = hash((args, tuple(sorted(kwargs.items()))))
            try:
                value, set_time = cache[key]
                if (time.time() - set_time) > self.timeout:
                    raise KeyError

            except KeyError:
                value, set_time = cache[key] = func(*args, **kwargs), time.time()

            return value

        return wrapped
