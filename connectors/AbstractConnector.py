# Local
from abc import ABC, abstractmethod
from classes import AbstractUser, SingletonMeta


class AbstractConnector(metaclass=SingletonMeta):
    def __init__(self):
        self.connections_cache = {}

    @abstractmethod
    def connect(self, user: AbstractUser):
        pass

    @abstractmethod
    def execute(self, user: AbstractUser, query):
        pass