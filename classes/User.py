import AbstractTransaction

class User(AbstractTransaction):
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.username = self.get_username()

    def create(self):
        query = f"INSERT INTO User (chat_id, username) VALUES ({self.chat_id}, '{self.username}')"
        return query

    def read(self):
        query = f"SELECT * FROM User WHERE chat_id = {self.chat_id}"
        return query

    def update(self):
        query = f"UPDATE User SET username = '{self.username}' WHERE chat_id = {self.chat_id}"
        return query

    def delete(self):
        query = f"DELETE FROM User WHERE chat_id = {self.chat_id}"
        return query

    def exit_demo_mode(self):
        pass

    def is_sheets_on(self):
        pass

    def get_user_creds(self):
        pass

    def get_user_sheetsFile(self):
        pass

    def get_username(self):
        pass

    def get_user_categories(self):
        pass

    def user_exists(self):
        pass