import re
import requests
from datetime import datetime
from itertools import groupby


def start_handler(user, update):
    url = 'http://127.0.0.1:8000/client/clients/'
    data = user_data_serializer(user)
    requests.post(url, json=data)
    deep_linking_query = update.effective_message.text
    param = re.search('/start (.+)', deep_linking_query).group(1)
    user_id = update.effective_user.id
    if param[0:9] == 'addmaster':
        master_nickname = param[10:]
        add_master_via_link(user_id, master_nickname)
    if param[0:4] == 'code':
        code = param[5:]
        username = update.effective_user.username
        try_to_assign_code(user_id, username, code)


def add_master_via_link(user_id, master_nickname):
    get_id_by_nickname = 'http://127.0.0.1:8000/client/add_master/get_id/'
    get_masters_url = f'http://127.0.0.1:8000/client/add_master/{user_id}'
    master_dict = {"nickname": master_nickname}
    master_id = requests.get(get_id_by_nickname, json=master_dict).json()
    masters_list = requests.get(get_masters_url).json()['master']
    if master_id not in masters_list:
        masters_list.append(master_id)
    data = {
        "client_telegram_id": user_id,
        "master": masters_list
    }
    requests.patch(get_masters_url, json=data)


def try_to_assign_code(user_id, username, code):
    url = 'http://127.0.0.1:8000/master/addmastertelegram/'
    data = {
        "master_telegram_id": user_id,
        "master_telegram_nickname": username,
        "verify_code": code
    }
    requests.patch(url, json=data)


def user_data_serializer(user):
    client_telegram_id = user.id
    client_telegram_nickname = user.username
    data = {
        "client_telegram_id": client_telegram_id,
        "client_telegram_nickname": client_telegram_nickname
    }
    return data


#  My_masters branch
def get_skills(master_id):
    get_master_skills_url = f'http://127.0.0.1:8000/master/services/?master_id={master_id}'
    skills = requests.get(get_master_skills_url).json()
    return skills


def get_masters(user):
    client_telegram_id = user.id
    url = f'http://127.0.0.1:8000/client/master_list/{client_telegram_id}'
    masters_list = requests.get(url).json()
    return masters_list


def remove_master(user, master_id):
    client_telegram_id = user.id
    url = f'http://127.0.0.1:8000/client/add_master/{client_telegram_id}'
    masters_list = requests.get(url).json()['master']
    masters_list.remove(int(master_id))
    data = {
        "client_telegram_id": client_telegram_id,
        "master": masters_list
    }
    requests.patch(url, json=data)


ONE_HOUR_SECONDS_COUNT = 3600


def get_datetime_list(master_id, skill_id):
    schedule_url = f'http://127.0.0.1:8000/schedule/by_master/{master_id}'
    service_url = f'http://127.0.0.1:8000/master/detail/?service={skill_id}'
    schedule_data = requests.get(schedule_url).json()
    service_data = requests.get(service_url).json()
    duration = service_data[0]['duration']
    datetime_objects = []

    # parsing request content for filling the list of slots with datetime objects
    for timeslot in schedule_data:
        datetime_obj = datetime.strptime(timeslot['datetime_slot'], '%Y-%m-%dT%H:%M:%SZ')
        datetime_objects.append(datetime_obj)
    # result list of timeslots
    timeslots = []
    # skipping long check procedure if duration equals 1 hour
    if duration == 1:
        timeslots = datetime_objects
    else:
        # checking every timeslot
        for i in range(len(datetime_objects)):
            # list of available timeslots belonging in the following range
            temp_list = []
            # checking next `duration` elements
            for j in range(duration):
                try:
                    # checking if the following slot is exactly 1 hour away
                    if (datetime_objects[i+j+1] - datetime_objects[i+j]).seconds == ONE_HOUR_SECONDS_COUNT:
                        # if the temp element satisfies the condition, it goes to the list
                        temp_list.append(datetime_objects[i])
                    # if the following temp slot is 1+ hour away, skip the rest as there's no reason to check further
                    else:
                        break
                # same goes for the case when we run of out list range
                except IndexError:
                    break
                # if (amount_of_next_available_slots + 1) equals duration, add the slot to the result list
                # (for example, 2 hour long service needs 1 extra slot)
                if (len(temp_list)+1) == duration:
                    timeslots.append(datetime_objects[i])
    return timeslots


def get_dates(master_id, skill_id):
    timeslots = get_datetime_list(master_id, skill_id)
    dates = [timeslot.date() for timeslot in timeslots]
    dates = [el for el, _ in groupby(dates)]
    return dates


def get_times(master_id, skill_id, date):
    timeslots = get_datetime_list(master_id, skill_id)
    assigned_timeslots = [timeslot for timeslot in timeslots if str(timeslot.date()) == date]
    return assigned_timeslots


def make_order(user, callback_data):
    url = 'http://127.0.0.1:8000/order/create/'
    user_id = user.id
    master_id = re.search(r"%(.+?)_mstr", callback_data).group(1)
    skill_id = re.search(r"mstr_(.+?)_skl", callback_data).group(1)
    datetime_info = re.search(r"skl_(.+)_dtmc", callback_data).group(1)
    start_datetime_object = datetime.strptime(datetime_info, '%Y-%m-%d %H:%M:%S')
    start_datetime_string = datetime.strftime(start_datetime_object, '%Y-%m-%dT%H:%M:%SZ')
    data = {
        "client_telegram_id": user_id,
        "master": master_id,
        "service": skill_id,
        "start_datetime_slot": start_datetime_string
    }
    requests.post(url, json=data)


def get_service_info(skill_id):
    url = f'http://127.0.0.1:8000/master/detail/?service={skill_id}'
    data = requests.get(url).json()[0]
    title = data['title']
    price = data['price']
    description = data['description']
    duration = data['duration']
    if duration == 1:
        plural = 'часа'
    else:
        plural = 'часов'
    text = f'Наименование: {title}\n' \
           f'Описание: {description}\n' \
           f'Стоимость: {price}\n' \
           f'Продолжительность: до {duration} {plural}'
    return text

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
