import json
from typing import List
from models import User
import os

USER_FILE = "users.json"

def load_users() -> List[User]:
    if not os.path.exists(USER_FILE):
        return []  # if no file yet, return empty list
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # file exists but empty or broken
        return []

def save_users(users: List[User]):
    with open(USER_FILE, "w") as f:
        json.dump([u.dict() for u in users], f, indent=2)

def find_users(filters: dict):
    users = load_users()
    print("User data for list", users)
    if not any(filters.values()):
        return users
    result = []
    for user in users:
        if not isinstance(user, dict):
            user = dict(user)
        match = True
        for key, value in filters.items():
            print('User detail', user)
            if value and str(user.get(key, "")).lower() != str(value).lower():
                match = False
                break
        if match:
            result.append(user)
    return result

def add_user(user: User):
    print("Adding user", user, type(user))
    users = load_users()
    print("Users List", type(users))
    user['id'] = len(users) + 1 if int(len(users)) else 1
    user_obj = User(**user)
    users.append(user_obj)
    save_users(users)
