from classes import Expense, Income, User, AbstractCRUD, AbstractUser
from remodel import SQLDataSource, DataSource
from decorators import SheetsDecorator

class Controller:
    def __init__(self) -> None:
        self.dsource_base = SQLDataSource()
        self.dsources = []

    def _get_dsource(self, user: AbstractUser) -> DataSource:
        dsource = self.dsource_base
        dsource = SheetsDecorator(dsource)
        return dsource

    def _create_datasource(self, user: AbstractUser) -> DataSource:
        dsource = SQLDataSource()
        return dsource

    def create(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
        print("Controller: Expense created")
        user = self.read(user)
        dsource = self._get_dsource(user)
        
        return dsource.create(user, obj)
        
    
    def read(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
        print("Controller: Expense read")
        if obj is None:
            user = self.read(user, user)
            ds = self._get_dsource(user)
            return ds.read(user, user)
        else:
            return self.dsource_base.read(user, obj)
        
        