import json

def get_users():
    with open('zoro3sr-app/users.json', 'r') as f:
        return json.load(f)

def check_credentials(username, password):
    users = get_users()
    if username in users and users[username] == password:
        return True
    return False
