from abc import ABC, abstractmethod
from classes import AbstractCRUD, AbstractUser
from datetime import date as Date

class AbstractTransaction(AbstractCRUD):
    @abstractmethod
    def get_month_transactions(self, user: AbstractUser, month: Date):
        pass

    @abstractmethod
    def get_range_transactions(self, user: AbstractUser, month_start: Date, month_end: Date):
        pass

    @abstractmethod
    def get_all_transactions(self, user: AbstractUser):
        pass

    @abstractmethod
    def get_avg_month_transactions(self, user: AbstractUser):
        pass