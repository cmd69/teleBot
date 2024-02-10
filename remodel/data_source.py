from abc import ABC, abstractmethod
from classes import AbstractCRUD

class DataSource(ABC):

    # ---- CRUD operations ---- #

    @abstractmethod
    def create(self, obj: AbstractCRUD):
        pass

    @abstractmethod
    def read(self, obj):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def delete(self, obj):
        pass

    # ---- SQL Specific operations ---- #

    @abstractmethod
    def get_expenses_by_month(self):
        pass

    @abstractmethod
    def get_incomes_by_month(self, chatID, date):
        pass

    @abstractmethod
    def get_all_expenses(self, chatID):
        pass

    @abstractmethod
    def get_all_incomes(self, chatID):
        pass
    
    @abstractmethod
    def get_all_categories(self):
        pass

    @abstractmethod
    def get_average_category_expense(self, chatID):
        pass

