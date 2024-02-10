from decorators import SheetsDecoratorInterface
from remodel import DataSource, DataSourceDecorator
from classes import Expense, Income

class SheetsDecorator(DataSourceDecorator, SheetsDecoratorInterface):
    """
    Concrete Decorators call the wrapped object and alter its result in some
    way.
    """

    def __init__(self, component: DataSource) -> None:
        super().__init__(component)


    def create(self, obj: str) -> str:
        """
        Decorators may call parent implementation of the operation, instead of
        calling the wrapped object directly. This approach simplifies extension
        of decorator classes.
        """
        print(f"Creating {obj} in Google Sheets")
        return self._component.create(obj)

    def new_expense(self, expense: Expense) -> bool:
        print(f"Creating {Expense} in Google Sheets")
        return True

    def new_income(self, income: Income) -> bool:
        print(f"Creating {income} in Google Sheets")
        return True

    def update_month_sheet(self, month: str):
        print(f"Updating {month} sheet")
        return True

    def create_next_month_sheet(self):
        print("Creating current month sheet")
        return "Creating current month sheet"

    def update_datatables(self):
        pass

    def update_all_sheets(self):
        pass

    def set_average_category_expense(self, chatID):
        pass

    def set_diesel_expenses(self):
        pass

    def set_incomes_vs_expenses(self):
        pass

    def set_networth_vs_savings(self):
        pass
