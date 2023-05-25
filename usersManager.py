import json


# ----------- USERS DATA ACCESS  --------------- #

import json

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

def userJsonON(mode, chatID):
    
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["jsonDatabase"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve user data for chatID {chatID}: {e}")

        
def userSheetsON(mode, chatID):
    if mode == 'dev':
        json_file = 'database/dev/users.json'
    else:
        json_file = 'database/prod/users.json'

    try:
        data = load_json(json_file)
        return data[str(chatID)]["sheetsDatabase"]
    except (FileNotFoundError, KeyError) as e:
        # Handle the error as per your application's requirements
        # For example, you can log the error or raise a custom exception
        raise RuntimeError(f"Failed to retrieve user data for chatID {chatID}: {e}")

def getUserData(mode, chatID):
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

def getUserCreds(mode, chatID):
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

def getUserName(mode, chatID):
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

def getUserDateFormat(mode, chatID):
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

def getUserExpensesFile(mode, chatID):
    json_file = 'database/dev/users.json' if mode == 'dev' else 'database/prod/users.json'
    try:
        with open(json_file) as f:
            data = json.load(f)
            return data[str(chatID)]["expensesFile"]
    except FileNotFoundError:
        raise Exception("User expenses file not found.")
    except (KeyError, ValueError):
        raise Exception("Invalid JSON format in user expenses file.")


def getUserCategoriesFile(mode, chatID):
    json_file = 'database/dev/users.json' if mode == 'dev' else 'database/prod/users.json'
    try:
        with open(json_file) as f:
            data = json.load(f)
            return data[str(chatID)]["categories"]
    except FileNotFoundError:
        raise Exception("User categories file not found.")
    except (KeyError, ValueError):
        raise Exception("Invalid JSON format in user categories file.")


def getUserCategories(mode, chatID):
    try:
        file = getUserCategoriesFile(mode, chatID)
        with open(file) as f:
            data = json.load(f)

        categories = [elem["category"] for elem in data]
        return categories
    except FileNotFoundError:
        raise Exception("Categories file not found.")
    except (KeyError, ValueError):
        raise Exception("Invalid JSON format in categories file.")



def userExists(mode, chatID):
    try:
        with open('database/dev/users.json' if mode == 'dev' else 'database/prod/users.json') as f:
            data = json.load(f)
            return str(chatID) in data
    except FileNotFoundError:
        raise Exception("Users file not found.")
    except (KeyError, ValueError):
        raise Exception("Invalid JSON format in users file.")

# ----------- END USERS DATA ACCESS  --------------- #