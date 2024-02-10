from abc import ABC, abstractmethod

class AbstractDBStrategy(ABC):
    
    # --- USER --- #
    @abstractmethod
    def create_user(self, user):
        pass
    # --- END USER --- #



    # --- EXPENSE --- #
    @abstractmethod
    def create_expense(self, expense):
        pass
    
    @abstractmethod
    def read_expense(self, expense):
        pass
    
    @abstractmethod
    def update_expense(self, expense):
        pass

    @abstractmethod
    def delete_expense(self, expense):
        pass
    # --- END EXPENSE --- #



    # --- INCOME --- # 
    @abstractmethod
    def create_income(self, income):
        pass
    
    @abstractmethod
    def read_income(self, income):
        pass
    
    @abstractmethod
    def update_income(self, income):
        pass

    @abstractmethod
    def delete_income(self, income):
        pass
    # --- END INCOME --- #


    # --- STREAMLIT --- #
    @abstractmethod
    def create_link(self, chatID):
        pass

    @abstractmethod
    def get_link(self, chatID):
        pass

    @abstractmethod
    def get_chatID_from_token(self, token):
        pass
    # --- END STREAMLIT --- #

    