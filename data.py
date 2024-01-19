import json


def install_users_data():
    try:
        with open('users_data.json', 'r') as f:
            users_data = json.load(f)
    except:
        users_data = {}
    return users_data


def save_users_data(users_data):
    with open('users_data.json', 'w') as f:
        json.dump(users_data, f)


def install_quest():
    with open('quest.json', 'r', encoding='utf-8') as f:
        quest = json.load(f)
        return quest
