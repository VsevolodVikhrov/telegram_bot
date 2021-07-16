import functools
from config import DEBUG as DEBUG


def debug_decorator(func):
    @functools.wraps(func)
    def wrapper(mock, *args, **kwargs):
        if DEBUG:
            return mock(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
