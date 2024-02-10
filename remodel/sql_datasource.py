from remodel import DataSource
from classes import AbstractCRUD


class SQLDataSource(DataSource):
    """
    Concrete Components provide default implementations of the operations. There
    might be several variations of these classes.
    """

    # ---- CRUD operations ---- #

    def create(self, obj: AbstractCRUD) -> str:
        obj.create()
        return "Nuevo gasto creado en SQLDataSource"
    
    def read(self, obj: AbstractCRUD) -> str:
        obj = obj.read()

        
        
    
    def update(self, obj: AbstractCRUD) -> str:
        obj.update()
        return "Actualizando gasto en SQLDataSource"
    
    def delete(self, obj: AbstractCRUD) -> str:
        obj.delete()
        return "Eliminando gasto en SQLDataSource"
    

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