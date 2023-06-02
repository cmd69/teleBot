import json


class UsersManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.users_data = self.load_json(self.db_path)

    def load_json(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data

    def create_new_user(self, new_user):        
        pass

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
