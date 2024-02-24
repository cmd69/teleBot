from remodel import DataSource
from classes import AbstractCRUD, AbstractUser
from connectors import SqliteConnector
from classes import User, AbstractTransaction, AbstractUser, Expense
from datetime import date as Date

class SQLDataSource(DataSource):

    def __init__(self):
        self.connection = SqliteConnector()

    # ---- CRUD operations ---- #

    def create(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
        query = obj.create()
        return self.connection.execute(user, *query)
    
    def read(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
        query = user.read() if obj is None else obj.read()
        return self.connection.execute(user, query)
    
    def update(self, user: AbstractUser, obj: AbstractCRUD=None) -> AbstractCRUD:
        query = user.update() if obj is None else obj.update()
        return self.connection.execute(user, query)
    
    def delete(self, user: AbstractUser, obj: AbstractCRUD=None) -> AbstractCRUD:
        query = user.delete() if obj is None else obj.delete()
        return self.connection.execute(user, query)
    

    # ---- SQL Specific operations ---- #

    def get_month_transactions(self, user: AbstractUser, transaction: type[AbstractTransaction], month: Date):
        query = transaction.get_month_transactions(user, month)

        return self.connection.execute(user, query)

    def get_range_transactions(self,user: AbstractUser, 
                               transaction: AbstractTransaction,
                               month_start: Date,
                               month_end: Date):
        
        pass

    def get_all_transactions(self, user: AbstractUser):
        pass

    def get_avg_month_transactions(self, user: AbstractUser):
        pass
    

    # ---- USER Related Operations ---- #

    def get_user_decorators(self, user: AbstractUser):
        return False
    
