import functools
from config import DEBUG as DEBUG
import mocks


def debug_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        source = None
        if DEBUG:
            source = mocks
            return func(*args, **kwargs, source=source)
    return wrapper
