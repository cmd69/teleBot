import json
import hashlib
import time
from utils import DecimalEncoder



class UsersManager:
    def __init__(self, db_path, port, ip):
        self.db_path = db_path
        self.port = port
        self.ip = ip
        self.users_data = self.load_json(self.db_path)

    def load_json(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data

    def create_new_user(self, new_user):        
        pass

    # Streamlit links management
    def get_link(self, chatID):
        try:
            data = self.users_data
            link = self.ip + ":" + self.port + "/?access_token=" + data['streamlit_keys'][str(chatID)]['token']
            return link
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {chatID}: {e}")
        

    def create_link(self, chatID):
        # token generation
        timestamp = str(time.time())
        token_data = str(chatID) + timestamp
        access_token = hashlib.sha256(token_data.encode()).hexdigest()

        # Updating streamlit keys
        try:
            data = self.users_data
            if "streamlit_keys" not in data:
                data["streamlit_keys"] = {}

            data["streamlit_keys"][str(chatID)] = {"date": timestamp, "token": access_token}
            self._save_data(data)
            return self.get_link(chatID)

        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {chatID}: {e}")


    def get_chatID_from_token(self, token):
        self.users_data = self.load_json(self.db_path)
        try:
            data = self.users_data
            for key, values in data["streamlit_keys"].items():
                if values['token'] == token:
                    return key
            return False

        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {token}: {e}")
        

        
    # END streamlit links management

    def user_json_on(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["jsonDatabase"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {chatID}: {e}")

    def user_sheets_on(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["sheetsDatabase"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {chatID}: {e}")

    def get_user_sheetsFile(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["sheetsFile"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user data for chat ID {chatID}: {e}")

    def get_user_creds(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["credFile"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user credentials for chat ID {chatID}: {e}")

    def get_user_name(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["username"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve username for chat ID {chatID}: {e}")

    def get_user_date_format(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["dateFormat"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve user date format for chat ID {chatID}: {e}")

    def get_user_expenses_file(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["expensesFile"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve expenses file for chat ID {chatID}: {e}")

    def get_user_categories_file(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["categories"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve categories file for chat ID {chatID}: {e}")

    def get_user_date_format(self, chatID):
        try:
            data = self.users_data
            return data[str(chatID)]["dateFormat"]
        except (FileNotFoundError, KeyError) as e:
            raise RuntimeError(f"Failed to retrieve categories file for chat ID {chatID}: {e}")

    def get_all_user_categories(self, chatID):
        try:
            file = self.get_user_categories_file(chatID)
            with open(file) as f:
                data = json.load(f)
            return data

        except FileNotFoundError:
            raise Exception("Categories file not found.")
        except (KeyError, ValueError):
            raise Exception("Invalid JSON format in categories file.")

    def get_user_categories(self, chatID):
        try:
            file = self.get_user_categories_file(chatID)
            with open(file) as f:
                data = json.load(f)

            categories = [elem["category"] for elem in data]
            return categories
        except FileNotFoundError:
            raise Exception("Categories file not found.")
        except (KeyError, ValueError):
            raise Exception("Invalid JSON format in categories file.")

    def user_exists(self, chatID):
        try:
            data = self.users_data
            return str(chatID) in data
        except FileNotFoundError:
            raise Exception("Users file not found.")
        except (KeyError, ValueError):
            raise Exception("Invalid JSON format in users file.")

    def _save_data(self, data):
        
        filename = self.db_path
        with open(filename, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4, cls=DecimalEncoder)
            file.truncate()    
        return True