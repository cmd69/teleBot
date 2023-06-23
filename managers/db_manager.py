# Local
from managers.json_manager import JsonManager
from managers.sheets_manager import SheetsManager

# Libraries
import datetime
import time


class DBManager:
    def __init__(self, users_manager, mode):
        self.mode = mode
        self.users_manager = users_manager
        self.json_manager = JsonManager(self.mode, self.users_manager)
        self.sheets_manager = SheetsManager(self.mode, self.users_manager)

    def set_users_manager(self, users_manager):
        self.users_manager = users_manager
    
    def get_users_manager(self):
        return self.users_manager

    # Streamlit links management
    def get_link(self, chatID):
        return self.users_manager.get_link(chatID)

    def create_link(self, chatID):
        return self.users_manager.create_link(chatID)

    def get_chatID_from_token(self, token):
        return self.users_manager.get_chatID_from_token(token)
    # END streamlit links management

    
    def user_exists(self, chatID):
        return self.users_manager.user_exists(chatID)

    def add_expense(self, chatID, expense):
        if self.users_manager.user_json_on(chatID):
            self.json_manager.add_expense(chatID, expense)
        if self.users_manager.user_sheets_on(chatID):
            self.sheets_manager.add_expense(chatID, expense)

    def add_income(self, chatID, income):
        if self.users_manager.user_json_on(chatID):
            self.json_manager.add_income(chatID, income)
        if self.users_manager.user_sheets_on(chatID):
            self.sheets_manager.add_income(chatID, income)

    def delete_expense(self, chatID, expense):
        if self.users_manager.user_json_on(chatID):
            self.json_manager.delete_expense(chatID, expense)
        if self.users_manager.user_sheets_on(chatID):
            self.sheets_manager.delete_expense(chatID, expense)

    def delete_income(self, chatID, income):
        if self.users_manager.user_json_on(chatID):
            self.json_manager.delete_income(chatID, income)
        if self.users_manager.user_sheets_on(chatID):
            self.sheets_manager.delete_income(chatID, income)

    def load_expenses_from_sheets_to_json(self, chatID):
        if self.users_manager.user_json_on(chatID):
            dates_to_load = self.sheets_manager.get_sheets_names(chatID)
            
            self.json_manager.delete_all(chatID)
        
            try:
                for date in dates_to_load:

                    formatted_expenses = self._format_sheets_to_json(
                        self.sheets_manager.get_expenses_by_month(chatID, date)
                    )
                    
                    self.json_manager.set_month_expenses(chatID, formatted_expenses)
                    
                    formatted_incomes = self._format_sheets_income_to_json(
                        self.sheets_manager.get_incomes_by_month(chatID, date)
                    )
                    
                    self.json_manager.set_month_incomes(chatID, formatted_incomes)

                return True
            except Exception as e:
                print("An error occurred transfering sheets to json:", str(e))
                return False

    def get_expenses_by_month(self, chatID, consult):
        if self.users_manager.user_json_on(chatID):
            return self._filter_expenses(
                self.json_manager.get_expenses_by_month(chatID, consult['date']),
                consult['category'],
                consult['subcategory']
            )
        return []

    def get_incomes_by_month(self, chatID, consult):
        if self.users_manager.user_json_on(chatID):
            return self.json_manager.get_incomes_by_month(chatID, consult['date'])
        return []

    def get_all_expenses(self, chatID):
        if self.users_manager.user_json_on(chatID):
            return self.json_manager.get_all_expenses(chatID)
        return []

    def get_expenses_from_sheets(self, chatID, consult):
        
        if self.users_manager.user_sheets_on(chatID):    
            
            formatted_expenses = self._format_sheets_to_json(
                self.sheets_manager.get_expenses_by_month(chatID, consult['date'])
            )

            return self._filter_expenses(
                formatted_expenses,
                consult['category'],
                consult['subcategory']
            )
        return []

    def get_expenses_from_json(self, chatID, consult):
        if self.users_manager.user_json_on(chatID):
            return self._filter_expenses(
                self.json_manager.get_expenses_by_month(chatID, consult['date']),
                consult['category'],
                consult['subcategory']
            )
        return []

    def _filter_expenses(self, expenses, category, subcategory):
        # round(float(m['totalIncome']),2), round(float(m['totalExpenses']),2)
        filtered = []
        
        try:
            # Caso base, no filtramos nada
            if (category == "Todas"):
                return expenses
            
            # Buscar gastos de 1 categoria sin subcategorias o
            # Buscar gastos 1 categoria con todas sus subcategorias
            elif (not subcategory or subcategory == "Todas"):
                for elem in expenses:
                    if (elem['category'] == category):
                        filtered.append(elem)
            
            # Buscar gastos 1 categoria (1+ subcategorias)
            else:
                # itero los gastos en busca de la subcategoria
                for elem in expenses:

                    if (elem['subcategory'] == subcategory):
                        filtered.append(elem)

            return filtered
        except:
            return []

    def _format_sheets_to_json(self, expenses):
        
        def convert_xls_datetime(xls_date):
            return (datetime.datetime(1899, 12, 30)
                + datetime.timedelta(days=xls_date))

        json_objects = []
        try:
            for item in expenses:
                
                date = item[0]
                if type(date) == int:
                    date = convert_xls_datetime(date)
                    date = datetime.datetime.strftime(date, "%d/%m/%Y")
                    date = str(date)

                json_object = {
                    "date": date,
                    "category": item[1],
                    "subcategory": item[2],
                    "price": item[3],
                    "description": item[4]
                }
                json_objects.append(json_object)
        
            return json_objects
        
        except:
            return []
    
    # TODO: merge with previous method
    def _format_sheets_income_to_json(self, incomes):
        
        def convert_xls_datetime(xls_date):
            return (datetime.datetime(1899, 12, 30)
                + datetime.timedelta(days=xls_date))
    
        json_objects = []
        try:
            for item in incomes:
                
                date = item[0]
                if type(date) == int:
                    date = convert_xls_datetime(date)
                    date = datetime.datetime.strftime(date, "%d/%m/%Y")
                    date = str(date)

                json_object = {
                    "date": date,
                    "price": item[1],
                    "description": item[2]
                }
                json_objects.append(json_object)
        
            return json_objects
        
        except:
            return []