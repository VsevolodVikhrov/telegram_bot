import functools
from config import DEBUG
import mocks, data_processing


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
        source = data_processing
        if DEBUG:
            source = mocks
        else:
            source = data_processing  # подразумевается присваивание файла с функциями запросов на бэкэнд
        return function(*args, **kwargs, source=source)
    return wrapper
