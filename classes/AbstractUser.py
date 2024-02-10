from abc import ABC, abstractmethod
from classes import AbstractCRUD

class AbstractUser(AbstractCRUD):
    # --- Setters --- #
    @abstractmethod
    def set_username(self):
        pass

    @abstractmethod
    def set_user_creds(self):
        pass

    @abstractmethod
    def set_user_sheetsFile(self):
        pass

    # --- Getters --- #
    @abstractmethod
    def get_user_creds(self):
        pass

    @abstractmethod
    def get_user_sheetsFile(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_user_categories(self):
        pass

    # --- User specific methods --- #
    @abstractmethod
    def exit_demo_mode(self):
        pass

    @abstractmethod
    def sheets_on(self):
        pass

    @abstractmethod
    def user_exists(self):
        pass