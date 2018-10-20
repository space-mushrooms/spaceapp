__all__ = ['cron_job', 'register_cron',
           'every_1minute_job', 'every_2minute_job', 'every_5minute_job', 'every_30minutes_job', 'every_hour_job',
           'every_night_job', 'every_morning_job']

# storage for all jobs
_cron_jobs = {}


class cron_job:
    default_cron_string = None

    def __init__(self, cron_string=default_cron_string, queue='default', args=None, kwargs=None,
                 repeat=None, id=None, timeout=None, description=None):
        self.cron_string = cron_string or self.default_cron_string
        self.queue = queue
        self.args = args
        self.kwargs = kwargs
        self.repeat = repeat
        self.id = id
        self.timeout = timeout
        self.description = description

    def __call__(self, f):
        self._register_job(f)
        return f

    def _register_job(self, f):
        func_name = f.__module__ + '.' + f.__name__
        if func_name in _cron_jobs:
            raise AttributeError('Such job already registered: {}'.format(func_name))

        _cron_jobs[func_name] = f, self


def register_cron(scheduler):
    for job, params in _cron_jobs.values():
        scheduler.cron(
            cron_string=params.cron_string,
            queue_name=params.queue,
            func=job,
            args=params.args,
            kwargs=params.kwargs,
            timeout=params.timeout,
            id=params.id,
            description=params.description or job.__doc__
        )


# some shortcuts
class every_1minute_job(cron_job):
    default_cron_string = '*/1 * * * *'


class every_2minute_job(cron_job):
    default_cron_string = '*/2 * * * *'


class every_5minute_job(cron_job):
    default_cron_string = '*/5 * * * *'


class every_30minutes_job(cron_job):
    default_cron_string = '*/30 * * * *'


class every_hour_job(cron_job):
    default_cron_string = '0 * * * *'


class every_night_job(cron_job):
    default_cron_string = '0 4 * * *'  # 4:00 MSK - 1:00 UTC


class every_morning_job(cron_job):
    default_cron_string = '0 8 * * *'  # 8:00 MSK - 5:00 UTC


class every_month_job(cron_job):
    default_cron_string = '0 8 1 * *'
