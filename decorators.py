import functools
import config
import mocks


def get_data_source(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        source = None  # подразумевается присваивание файла с функциями запросов на бэкэнд
        if config.DEBUG:
            source = mocks
        return function(*args, **kwargs, source=source)

