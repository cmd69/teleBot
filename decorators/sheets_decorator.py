from decorators import SheetsDecoratorInterface
from remodel import DataSource, DataSourceDecorator
from classes import Expense, Income, AbstractCRUD, AbstractUser
from connectors import SheetsConnector


class SheetsDecorator(DataSourceDecorator, SheetsDecoratorInterface):
    """
    Concrete Decorators call the wrapped object and alter its result in some
    way.
    """

    def __init__(self, component: DataSource) -> None:
        super().__init__(component)
        self.connection = SheetsConnector()



    # def create(self, obj: str) -> str:
    #     """
    #     Decorators may call parent implementation of the operation, instead of
    #     calling the wrapped object directly. This approach simplifies extension
    #     of decorator classes.
    #     """
    #     print(f"Creating {obj} in Google Sheets")
    #     return self._component.create(obj)
        
    def create(self, user: AbstractUser, obj: AbstractCRUD= None) -> bool:
        """
        Decorators may call parent implementation of the operation, instead of
        calling the wrapped object directly. This approach simplifies extension
        of decorator classes.
        """
        if obj:
            self.connection.execute(user, obj.create())
            print(f"Creating {obj} in Google Sheets")
            print(self._component)
        return self._component.create(user, obj)
        


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
