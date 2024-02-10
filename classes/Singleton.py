from abc import ABC, abstractmethod

class Singleton(ABC):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Singleton._instance:
            print('Initializing Singleton')
            Singleton._instance = self

            