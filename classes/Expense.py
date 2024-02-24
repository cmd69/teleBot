from classes import AbstractTransaction
from classes import AbstractUser
from datetime import date as Date

class Expense(AbstractTransaction):
    def __init__(self, chat_id, date, amount, description=None, id=None):
        self.id = id
        self.chat_id = chat_id
        self.date = date
        self.amount = amount
        self.description = description

    def create(self):
        query = f"INSERT INTO EXPENSE (chat_id, date, amount, description) VALUES (?, ?, ?, ?)"
        values = (self.chat_id, self.date, self.amount, self.description)
        return query, values

    def read(self):
        query = "SELECT * FROM EXPENSE WHERE id = ?"
        values = (self.id,)
        return query, values

    def update(self):
        query = "UPDATE EXPENSE SET chat_id = ?, date = ?, amount = ?, description = ? WHERE id = ?"
        values = (self.chat_id, self.date, self.amount, self.description, self.id)
        return query, values

    def delete(self):
        query = "DELETE FROM EXPENSE WHERE id = ?"
        values = (self.id,)
        return query, values
    
    @staticmethod
    def get_month_transactions(user: AbstractUser, month: Date):
        query = "SELECT * FROM EXPENSE WHERE chat_id = ?" 
        values = (user.chat_id)
        return query, values
    
    @staticmethod
    def get_range_transactions(user: AbstractUser, month_start: Date, month_end: Date):
        pass

    @staticmethod
    def get_all_transactions(user: AbstractUser):
        pass

    @staticmethod
    def get_avg_month_transactions(user: AbstractUser):
        pass