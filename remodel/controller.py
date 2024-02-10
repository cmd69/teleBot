from classes import Expense, Income, User, AbstractCRUD, AbstractUser


class Controller:
    def __init__(self) -> None:
        pass

    def _create_expense(self, expense: Expense) -> bool:
        pass

    def _create_datasource(self):
        pass

    def create_expense(self, expense: Expense, user: AbstractUser) -> bool:
        