from abc import ABC, abstractmethod
from remodel import DataSource

class SheetsDecoratorInterface(DataSource):
    @abstractmethod
    def update_month_sheet(self, month: str):
        pass
    
    @abstractmethod
    def create_next_month_sheet(self):
        pass

    @abstractmethod
    def update_datatables(self):
        pass

    @abstractmethod
    def update_all_sheets(self):
        pass

    @abstractmethod
    def set_average_category_expense(self, chatID):
        pass

    @abstractmethod
    def set_diesel_expenses(self):
        pass

    @abstractmethod
    def set_incomes_vs_expenses(self):
        pass

    @abstractmethod
    def set_networth_vs_savings(self):
        pass




