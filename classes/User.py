from classes import AbstractUser

class User(AbstractUser):
    def __init__(self, chat_id, username=None, sheets_file=None, credentials_path=None):
        self.chat_id = chat_id
        self.username = username
        self.sheets_file = sheets_file
        self.credentials_path = credentials_path


    # CRUD methods

    def create(self):
        query = f"INSERT INTO User (chat_id, username, sheets_file, credentials_path) VALUES ({self.chat_id}, '{self.username}', '{self.sheets_file}', '{self.credentials_path}')"
        return query

    def read(self):
        query = f"SELECT * FROM User WHERE chat_id = {self.chat_id}"
        return query

    def update(self):
        query = f"UPDATE User SET username = '{self.username}', sheets_file = '{self.sheets_file}', credentials_path = '{self.credentials_path}' WHERE chat_id = {self.chat_id}"
        return query

    def delete(self):
        query = f"DELETE FROM User WHERE chat_id = {self.chat_id}"
        return query

    # User specific methods

    # --- Setters --- #

    def set_username(self):
        pass

    def set_user_creds(self):
        pass

    def set_user_sheetsFile(self):
        pass

    # --- Getters --- #

    def get_user_creds(self):
        pass

    def get_user_sheetsFile(self):
        pass

    def get_username(self):
        pass

    def get_user_categories(self):
        pass

    # --- User specific methods --- #

    def exit_demo_mode(self):
        pass

    def sheets_on(self):
        pass

    def user_exists(self):
        pass