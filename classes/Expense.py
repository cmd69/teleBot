import AbstractTransaction

class Expense(AbstractTransaction):
    def __init__(self, chat_id, date, amount, category_id, subcategory_id=None, description=None, id=None):
        self.id = id
        self.chat_id = chat_id
        self.date = date
        self.amount = amount
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.description = description

    def create(self):
        query = f"INSERT INTO expenses (chat_id, date, amount, category_id, subcategory_id, description) VALUES ({self.chat_id}, '{self.date}', {self.amount}, {self.category_id}, {self.subcategory_id}, '{self.description}')"
        return query

    def read(self):
        query = f"SELECT * FROM expenses WHERE id = {self.id}"
        return query

    def update(self):
        query = f"UPDATE expenses SET chat_id = {self.chat_id}, date = '{self.date}', amount = {self.amount}, category_id = {self.category_id}, subcategory_id = {self.subcategory_id}, description = '{self.description}' WHERE id = {self.id}"
        return query

    def delete(self):
        query = f"DELETE FROM expenses WHERE id = {self.id}"
        return query
