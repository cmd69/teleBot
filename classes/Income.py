from classes import AbstractCRUD

class Income(AbstractCRUD):
    def __init__(self, chat_id, date, amount, description=None, id=None):
        self.id = id
        self.chat_id = chat_id
        self.date = date
        self.amount = amount
        self.description = description

    def create(self):
        query = "INSERT INTO INCOME (chat_id, date, amount, description) VALUES (?, ?, ?, ?)"
        values = (self.chat_id, self.date, self.amount, self.description)
        return query, values

    def read(self):
        query = "SELECT * FROM INCOME WHERE id = ?"
        values = (self.id,)
        return query, values

    def update(self):
        query = "UPDATE INCOME SET chat_id = ?, date = ?, amount = ?, description = ? WHERE id = ?"
        values = (self.chat_id, self.date, self.amount, self.description, self.id)
        return query, values

    def delete(self):
        query = "DELETE FROM INCOME WHERE id = ?"
        values = (self.id,)
        return query, values