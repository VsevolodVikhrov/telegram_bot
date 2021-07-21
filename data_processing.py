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
