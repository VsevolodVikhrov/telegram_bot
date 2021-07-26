import requests


def set_user_data(user):
    url = 'http://127.0.0.1:8000/client/clients/'
    data = user_data_serializer(user)
    return requests.post(url, json=data)


def user_data_serializer(user):
    client_telegram_id = user.id
    client_telegram_nickname = user.username
    data = {
        "client_telegram_id": client_telegram_id,
        "client_telegram_nickname": client_telegram_nickname
    }
    return data


#my orders data_processing

def get_orders(user_id):
    """
    Функция выполняет запрос к бэку передавая квери параметр client_telegram_id,
    полученный ответ сериализует в json
    """
    url = 'http://127.0.0.1:8000/order/orders/'
    data = serializer_client_id(user_id)
    return requests.get(url, params=data).json()


def serializer_client_id(user_id):
    """
    Функция создает словарик значение ключа "client_telegram_id" будет id клиента
    """
    client_telegram_id = user_id
    data = {
        "client_telegram_id": client_telegram_id,
        }
    return data


def get_order(order_id):
    """
    Функция выполняет запрос к бэку передавая квери параметр client_telegram_id,
    полученный ответ сериализует в json
    """
    url = f'http://127.0.0.1:8000/order/orders/{order_id}'
    return requests.get(url).json()


def serializer_order_info(retrieve_order_info):
    """
    Расспаковывает полученный json с информацией по заказу и превращает его
    в словарь по типу order в mocks.py
    """
    key = retrieve_order_info['id']
    order_dict = dict.fromkeys([key], [retrieve_order_info['master']['nickname'],
                                       retrieve_order_info['service']['title'],
                                       retrieve_order_info['service']['price']
                                       ])
    return order_dict


def delete_order(order_id):
    """
    Делает запрос на удаление заказа передавая order_id
    """
    url = f'http://127.0.0.1:8000/order/orders/{order_id}'
    return requests.delete(url)
