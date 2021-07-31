import requests
from datetime import datetime
from itertools import groupby


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



