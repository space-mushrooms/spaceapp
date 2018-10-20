import functools
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django_rq import get_queue, get_scheduler
from rq.compat import string_types
from rq.defaults import DEFAULT_RESULT_TTL

__all__ = ['job', 'run_task', 'config_task_and_run']

# storage for all jobs
_jobs = {}

# default value
_default = object()


def _value_or_default(value, default=None):
    return default if value is _default else value


class job:
    def __init__(self, name, queue='default', connection=None, timeout=None,
                 result_ttl=DEFAULT_RESULT_TTL, ttl=None, defer=None):
        """A decorator that adds a ``delay`` method to the decorated function,
        which in turn creates a RQ job when called. Accepts a required
        ``queue`` argument that can be either a ``Queue`` instance or a string
        denoting the queue name.  For example:

            @job(queue='default')
            def simple_add(x, y):
                return x + y

            simple_add.delay(1, 2) # Puts simple_add function into queue
        """
        self.queue = queue
        self.name = name
        self.connection = connection
        self.timeout = timeout
        self.result_ttl = result_ttl
        self.ttl = ttl
        self.defer = defer

    def __call__(self, f):
        self._register_job(f)

        def _schedule_job(func, *args, defer=self.defer, **kwargs):
            if settings.RQ_SYNC_MODE:
                return func(*args, **kwargs)

            scheduler = get_scheduler(self.queue)
            return scheduler.enqueue_in(timedelta(seconds=defer), func, *args, **kwargs)

        # run task with default configuration
        @functools.wraps(f)
        def delay(*args, **kwargs):
            if isinstance(self.queue, string_types):
                queue = get_queue(self.queue)
                if self.connection is None:
                    self.connection = queue.connection
            else:
                queue = self.queue
            depends_on = kwargs.pop('depends_on', None)

            if self.defer is not None:
                return _schedule_job(f, *args, defer=self.defer, **kwargs)

            if settings.RQ_SYNC_MODE:
                return f(*args, **kwargs)

            return queue.enqueue_call(f, args=args, kwargs=kwargs, timeout=self.timeout,
                                      result_ttl=self.result_ttl, ttl=self.ttl, depends_on=depends_on)

        # run task with different configuration
        @functools.wraps(f)
        def configured_delay(args, kwargs, queue=self.queue, timeout=self.timeout,
                             result_ttl=self.result_ttl, ttl=self.ttl, depends_on=None, defer=self.defer):
            # check if arguments are default
            args = _value_or_default(args) or ()
            kwargs = _value_or_default(kwargs) or {}
            depends_on = _value_or_default(depends_on)
            queue = _value_or_default(queue, self.queue)
            timeout = _value_or_default(timeout, self.timeout)
            result_ttl = _value_or_default(result_ttl, self.result_ttl)
            ttl = _value_or_default(ttl, self.ttl)
            defer = _value_or_default(defer, self.defer)

            if isinstance(queue, string_types):
                queue = get_queue(queue)
                if self.connection is None:
                    self.connection = queue.connection

            if defer is not None:
                return _schedule_job(f, *args, defer=defer, **kwargs)

            if settings.RQ_SYNC_MODE:
                return f(*args, **kwargs)

            return queue.enqueue_call(f, args=args, kwargs=kwargs, timeout=timeout,
                                      result_ttl=result_ttl, ttl=ttl, depends_on=depends_on)

        f.delay = delay
        f.configured_delay = configured_delay
        return f

    def _register_job(self, f):
        if self.name in _jobs:
            raise AttributeError('Such job already registered: {}'.format(self.name))

        _jobs[self.name] = f


def _transaction_on_commit(func, *args, **kwargs):
    task_func = lambda: func(*args, **kwargs)

    if settings.TESTING:
        return task_func()
    else:
        return transaction.on_commit(task_func)


def get_job(name):
    return _jobs[name]


def run_task(name, *args, **kwargs):
    _job = get_job(name)
    return _transaction_on_commit(_job.delay, *args, **kwargs)


def config_task_and_run(name, args=_default, kwargs=_default, queue=_default, timeout=_default,
                        result_ttl=_default, ttl=_default, depends_on=_default, defer=_default):
    _job = get_job(name)
    return _transaction_on_commit(_job.configured_delay, args=args, kwargs=kwargs, queue=queue, timeout=timeout,
                                  result_ttl=result_ttl, ttl=ttl, depends_on=depends_on, defer=defer)
