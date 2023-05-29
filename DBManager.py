from UsersManager import UsersManager
from JsonManager import JsonManager
from SheetsManager import SheetsManager
import datetime


class DBManager:
    def __init__(self, mode):
        self.mode = mode
        self.users_manager = UsersManager(self.mode)
        self.json_manager = JsonManager(self.mode, self.users_manager)
        self.sheets_manager = SheetsManager(self.mode, self.users_manager)

    def user_exists(self, chatID):
        return self.users_manager.user_exists(chatID)

    def get_user_categories(self, chatID):
        return self.users_manager.get_user_categories(chatID)

    def get_user_categories_file(self, chatID):
        return self.users_manager.get_user_categories_file(chatID)

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

    def load_expenses_from_sheets_to_json(self, chatID,):
        if self.users_manager.user_json_on(chatID):
            expenses = self.sheets_manager.get_all_expenses(chatID)
            self.json_manager.set_expenses(expenses)

    def get_expenses(self, chatID, consult):
        if self.users_manager.user_json_on(chatID):
            return self._filter_expenses(
                self.json_manager.get_expenses_by_month(chatID, consult['date']),
                consult['category'],
                consult['subcategory']
            )
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