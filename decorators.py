import functools
from config import DEBUG
import mocks


# decorator for add master and catalogue features
def debug_decorator(func):
    @functools.wraps(func)
    def wrapper(mock, *args, **kwargs):
        if DEBUG:
            return mock(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper


def get_data_source(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        source = None  # подразумевается присваивание файла с функциями запросов на бэкэнд
        if DEBUG:
            source = mocks
        return function(*args, **kwargs, source=source)
    return wrapper
