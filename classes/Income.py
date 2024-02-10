from classes import AbstractCRUD

class Income(AbstractCRUD):
    def __init__(self, chat_id, date, amount, description=None, id=None):
        self.id = id
        self.chat_id = chat_id
        self.date = date
        self.amount = amount
        self.description = description

    def create(self):
        query = f"INSERT INTO Income (chat_id, date, amount, description) VALUES ({self.chat_id}, '{self.date}', {self.amount}, '{self.description}')"
        return query

    def read(self):
        query = f"SELECT * FROM Income WHERE id = {self.id}"
        return query

    def update(self):
        query = f"UPDATE Income SET chat_id = {self.chat_id}, date = '{self.date}', amount = {self.amount}, description = '{self.description}' WHERE id = {self.id}"
        return query

    def delete(self):
        query = f"DELETE FROM Income WHERE id = {self.id}"
        return query