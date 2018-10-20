import os

# Must bypass this block if another settings module was specified.
if os.environ.get('DJANGO_SETTINGS_MODULE', 'settings') == 'settings':
    from .components.base import *
    from .components.database import *
    from .components.sentry import *
    from .components.logging import *
    from .components.auth import *
    from .components.redis import *
    from .components.redis_queue import *
    from .components.static import *
    from .components.images import *
    from .components.livesettings import *

    try:
        from .local import *
    except ImportError:
        pass
