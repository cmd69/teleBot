import json


# ----------- USERS DATA ACCESS  --------------- #

import json

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

def getUserData(chatID, mode='dev'):
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["credFile"], data[str(chatID)]["sheetsFile"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve user data for chatID {chatID}: {e}")

def getUserCreds(chatID, mode='dev'):
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["credFile"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve user credentials for chatID {chatID}: {e}")

def getUserName(chatID, mode='dev'):
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["username"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve username for chatID {chatID}: {e}")

def getUserDateFormat(chatID, mode='dev'):
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["dateFormat"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve user date format for chatID {chatID}: {e}")


# ----------- END USERS DATA ACCESS  --------------- #