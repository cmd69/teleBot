from classes import AbstractUser

class User(AbstractUser):
    def __init__(self, chat_id, username=None):
        self.chat_id = chat_id
        self.username = username


    # CRUD methods

    def create(self):
        query = f"INSERT INTO USER (chat_id, username) VALUES (?, ?)"
        values = (self.chat_id, self.username)
        return query, values

    def read(self):
        query = f"SELECT * FROM USER WHERE chat_id = ?"
        values = (self.chat_id,)
        return query, values

    def update(self):
        query = "UPDATE USER SET username = ? WHERE chat_id = ?"
        values = (self.username, self.chat_id)
        return query, values

    def delete(self):
        query = f"DELETE FROM USER WHERE chat_id = ?"
        values = (self.chat_id,)
        return query, values

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