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
