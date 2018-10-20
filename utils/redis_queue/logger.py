import logging

from rq import get_current_job


def get_task_logger(name=None):
    logger = logging.getLogger(name)
    base_log = logger._log

    def _log(level, msg, args, exc_info=None, extra=None, stack_info=False):
        job, id = get_current_job(), None
        if job:
            id = job.id
        if id:
            msg = '[{}] - {}'.format(id, msg)
        return base_log(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    logger._log = _log
    return logger
