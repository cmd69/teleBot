from remodel import DataSource
from classes import AbstractCRUD, AbstractUser
from connectors import SqliteConnector
from classes import User


class SQLDataSource(DataSource):
    """
    Concrete Components provide default implementations of the operations. There
    might be several variations of these classes.
    """

    def __init__(self):
        self.connection = SqliteConnector()

    # ---- CRUD operations ---- #

    def create(self, user: AbstractUser, obj: AbstractCRUD= None) -> str:
        print(obj)
        query = obj.create()
        self.connection.execute(user, query)
        return "Nuevo gasto creado en SQLDataSource"
    
    def read(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
        if obj is None:
            query = user.read()
        else:
            query = obj.read()
        
        print(query)
        return self.connection.execute(user, query)

        
        
    
    def update(self, user: AbstractUser, obj: AbstractCRUD=None) -> str:
        obj.update()
        return "Actualizando gasto en SQLDataSource"
    
    def delete(self, user: AbstractUser, obj: AbstractCRUD=None) -> str:
        obj.delete()
        return "Eliminando gasto en SQLDataSource"`
    

    # ---- SQL Specific operations ---- #

    def get_expenses_by_month(self):
        return "Getting expenses by month in SQLDataSource"
    
    def get_incomes_by_month(self, chatID, date):
        return "Getting incomes by month in SQLDataSource"

    def get_all_expenses(self, chatID):
        return "Getting all expenses in SQLDataSource"
    
    def get_all_incomes(self, chatID):      
        return "Getting all incomes in SQLDataSource"
    
    def get_all_categories(self):
        return "Getting all categories in SQLDataSource"
    
    def get_average_category_expense(self, chatID):
        return "Getting average category expense in SQLDataSource"