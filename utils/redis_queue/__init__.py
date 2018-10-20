from .cron import *
from .decorators import single_instance_task
from .jobs import *
from .logger import get_task_logger

default_app_config = 'utils.redis_queue.apps.RedusQueueAppConfig'
