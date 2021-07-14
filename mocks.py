masters_list_mock = ["Ihar", "Anton", "Lexa", "Seva"]


def get_masters():
    return masters_list_mock


def send_new_master(master_name: str):
    return True


categories_list = ['Makeup', 'Manicure', 'Pedicure', 'Brow enhancement',
                   'Cleaning', 'Hair care', 'Barber', 'Babysitting']


def get_catalogue_categories():
    return categories_list


category_masters = {
    'Makeup': ["Ihar"],
    'Manicure': ["Not Ihar", "Ihar"],
    'Pedicure': ["sdfdsf"],
    'Brow enhancement': ["asdfdasf", "smth", "asdsad"],
    'Cleaning': ["asdfdsf", "sdfdsf", "dsfdsfd"],
    'Hair care': ["13256", "lytbydr", "Ihar again"],
    'Barber': ["literally who?"],
    'Babysitting': ["sdf", "sdafdsfg", "afdfagasg", "dsfadsg", "sdfasdf", "sdfdasf"
                    "adsfadf", "asdfsdf"],
}


def get_category_masters(category):
    return category_masters[category]
