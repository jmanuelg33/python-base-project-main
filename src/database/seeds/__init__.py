from functools import wraps

from src import logger


def skip_if(condition):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if condition:
                logger.info(f"{func.__name__}.py skipped script")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
