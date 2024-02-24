from typing import Any
from classes import Expense, Income, User, AbstractCRUD, AbstractUser
from remodel import SQLDataSource, DataSource
from decorators import SheetsDecorator, SheetsDecoratorInterface

class Controller():
    def __init__(self) -> None:
        self.dsource_base = SQLDataSource()
        self.dsources = {}

    def __getattribute__(self, __name: str) -> Any:
        try:
            return object.__getattribute__(self, __name)
        except AttributeError:
            pass 
        
        def proxy(*args, **kwargs):
            dsource = self._get_dsource(args[0])
            attr = getattr(dsource, __name)

            if callable(attr):
                return attr(*args, **kwargs)
            else:
                raise AttributeError(f"Method {__name} is not available")
        
        return proxy

    def _get_dsource(self, user: AbstractUser) -> DataSource:
        if user in self.dsources:
            return self.dsources[user]
        else:
            dsource = self._create_datasource(user)
            self.dsources[user] = dsource
            return dsource

    def _create_datasource(self, user: AbstractUser) -> DataSource:
        
        dsource = SQLDataSource()
        sheets_on = self.dsource_base.get_user_decorators(user)
        
        if sheets_on:
            dsource = SheetsDecorator(dsource)
        
        self.dsources[user] = dsource
        
        return dsource

    # def create(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
    #     print("Controller: Expense created")
    #     user = self.read(user)
    #     dsource = self._get_dsource(user)
        
    #     return dsource.create(user, obj)
        
    
    # def read(self, user: AbstractUser, obj: AbstractCRUD= None) -> AbstractCRUD:
    #     print("Controller: Expense read")
    #     if obj is None:
    #         user = self.read(user, user)
    #         ds = self._get_dsource(user)
    #         return ds.read(user, user)
    #     else:
    #         return self.dsource_base.read(user, obj)
        
        
