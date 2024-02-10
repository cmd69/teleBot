# Local
from classes import AbstractCRUD
from remodel import DataSource

class DataSourceDecorator(DataSource):
    """
    Decorator class
    """
    _component = None

    def __init__(self, component: DataSource) -> None:
        self._component = component

    # def __getattr__(self, name):
    #     """
    #     Automatically delegate attribute access to the decorated component.
    #     This includes method calls for methods not overridden in the decorator.
    #     """
    #     print("getattr")
    #     return getattr(self._component, name)
    
    
    
    
    
    # ---- CRUD operations ---- #
    
    def create(self, obj: AbstractCRUD):
        return self._component.create(obj)
    
    def read(self, obj: AbstractCRUD):
        return self._component.read(obj)
    
    def update(self, obj: AbstractCRUD):
        return self._component.update(obj)
    
    def delete(self, obj: AbstractCRUD):
        return self._component.delete(obj)
    
    
    # ---- SQLDataSource default methods ---- #
    
    def get_expenses_by_month(self):
        return self._component.get_expenses_by_month()
    
    def get_incomes_by_month(self, chatID, date):
        return self._component.get_incomes_by_month(chatID, date)
    
    def get_all_expenses(self, chatID):
        return self._component.get_all_expenses(chatID)
    
    def get_all_incomes(self, chatID):
        return self._component.get_all_incomes(chatID)

    def get_all_categories(self):
        return self._component.get_all_categories()
    
    def get_average_category_expense(self, chatID):
        return self._component.get_average_category_expense(chatID)
    
    
    
    
    
    
    