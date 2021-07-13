masters_list_mock = ["Ihar", "Anton", "Lexa", "Seva"]
masters_skills_mock = {
    "Ihar": ["Nails", "French"],
    "Anton": ["Break the doors via leg", "Fix domofons"],
    "Lexa": ["Photohraphy", "Pivo"],
    "Seva": ["Coding", "Riding bike"]
                                           }
dates = ["08.06", "05.04", "03.08", "17.04", "15.12", "12.12", "19.12", "28.01", "12.05", "27.07", "13.05"]


def get_masters():
    return masters_list_mock


def get_skills(master):
    skills = masters_skills_mock[master]
    return skills


def get_dates(master, skill):
    return dates
