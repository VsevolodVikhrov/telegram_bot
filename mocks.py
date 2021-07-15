# My_masters feature mocks
masters_list_mock = ["Ihar", "Anton", "Lexa", "Seva"]
masters_skills_mock = {
    "Ihar": ["Nails", "French"],
    "Anton": ["Break the doors via leg", "Fix domofons"],
    "Lexa": ["Photohraphy", "Pivo", "Wine_tasting", "Hang out with extremists"],
    "Seva": ["Coding", "Riding bike"]
                                           }
dates = ["08.06", "05.04", "03.08", "17.04", "15.12", "12.12", "19.12", "28.01", "12.05", "27.07", "13.05"]
times = [str(time) for time in range(0, 24)]


def get_masters():
    return masters_list_mock


def get_skills(master):
    skills = masters_skills_mock[master]
    return skills


def get_dates(master, skill):
    return dates


def get_times(master, skill, date):
    return times

# My_orders feature mocks  
anton = 443993822
alex = 347083046
seva = 427279107
orders = {443993822: ['nails', 'make up', 'brows']}
order = {'nails': ['Algima', '25$', '20-07-2021', '17.00'],
         'make up': ['Julia', '40$', '21-07-2021', '10-00'],
         'brows': ['Anya', '23.5$', '21-07-2021', '21=00']
         }
orders2 = {443993822: []}


def get_orders(key: int) -> list:
    if key in orders:
        return orders[key]


def get_order(key: str) -> list:
    return order[key]
