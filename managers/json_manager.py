# Local
from managers.users_manager import UsersManager
from utils import DecimalEncoder

# Libraries
import json
import decimal
import datetime





class JsonManager:
    def __init__(self, mode, users_manager):
        self.mode = mode
        self.users_manager = users_manager

    def load_json(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data

    def add_expense(self, chatID, expense):
        
        expenses = self.load_json(self._get_filename(chatID))
        date = datetime.datetime.strptime(expense['date'], '%d/%m/%Y')
        year = date.year
        month = date.month
        
        for y in expenses['years']:
            if y['year'] == year:
                for m in y['months']:
                    if m['month'] == month:
                        m['expenses'].append(expense)
                        m['totalExpenses'] = decimal.Decimal(str(m['totalExpenses'])) + decimal.Decimal(str(expense['price']))
                        y['totalExpenses'] = decimal.Decimal(str(y['totalExpenses'])) + decimal.Decimal(str(expense['price']))
                        break
                else:
                    y['months'].append({
                        'month': month,
                        'expenses': [expense],
                        'income': [],
                        'totalExpenses': decimal.Decimal(str(expense['price'])),
                        'totalIncome': decimal.Decimal('0')
                    })
                    y['totalExpenses'] = decimal.Decimal(str(y['totalExpenses'])) + decimal.Decimal(str(expense['price']))
                break
        else:
            expenses['years'].append({
                'year': year,
                'months': [{
                    'month': month,
                    'expenses': [expense],
                    'income': [],
                    'totalExpenses': decimal.Decimal(str(expense['price'])),
                    'totalIncome': decimal.Decimal('0')
                }],
                'totalExpenses': decimal.Decimal(str(expense['price'])),
                'totalIncome': decimal.Decimal('0'),
                'savings': decimal.Decimal('0')
            })

        self._save_expenses(chatID, expenses)

    def add_income(self, chatID, income):
        
        expenses = self.load_json(self._get_filename(chatID))
        date = datetime.datetime.strptime(income['date'], '%d/%m/%Y')
        year = date.year
        month = date.month

        # Find the year and month in the income object
        # date_str = income['date']
        # day, month, year = map(int, date_str.split('/'))
        
        # Find the year index in the JSON structure
        year_index = None
        for i, year_data in enumerate(expenses['years']):
            if year_data['year'] == year:
                year_index = i
                break
        
        # If the year doesn't exist, add it to the JSON structure
        if year_index is None:
            year_data = {
                'year': year,
                'months': [],
                'totalExpenses': 0,
                'totalIncome': 0,
                'savings': 0
            }
            expenses['years'].append(year_data)
            year_index = len(expenses['years']) - 1
        
        # Find the month index in the year's months list
        month_index = None
        for i, month_data in enumerate(expenses['years'][year_index]['months']):
            if month_data['month'] == month:
                month_index = i
                break
        
        # If the month doesn't exist, add it to the year's months list
        if month_index is None:
            month_data = {
                'month': month,
                'expenses': [],
                'income': [],
                'totalExpenses': 0,
                'totalIncome': 0
            }
            expenses['years'][year_index]['months'].append(month_data)
            month_index = len(expenses['years'][year_index]['months']) - 1
        
        # Add the new income to the month's income list
        expenses['years'][year_index]['months'][month_index]['income'].append(income)
        
        # Update the total income for the month, year, and overall
        expenses['years'][year_index]['months'][month_index]['totalIncome'] += income['price']
        expenses['years'][year_index]['totalIncome'] += income['price']



        self._save_expenses(chatID, expenses)
        
    def delete_expense(self, chatID, expense):

        expenses = self.load_json(self._get_filename(chatID))
        date = datetime.datetime.strptime(expense['date'], '%d/%m/%Y')
        expense_year = date.year
        expense_month = date.month

        for year_data in expenses['years']:
            if year_data['year'] == expense_year:
                for month_data in year_data['months']:
                    if month_data['month'] == expense_month:
                        for i, current_expense in enumerate(month_data['expenses']):
                            if current_expense == expense:
                                month_data['expenses'].pop(i)  # Delete the expense
                                break
                        break
                break

        return self._save_expenses(chatID, expenses)
        
    def delete_income(self, chatID, income):
        data = self.load_json(self._get_filename(chatID))
        date = datetime.datetime.strptime(income['date'], '%d/%m/%Y')
        income_year = date.year
        income_month = date.month
        
        # Find the corresponding year and month in the JSON
        for year_data in data["years"]:
            if year_data["year"] == income_year:
                for month_data in year_data["months"]:
                    if month_data["month"] == income_month:
                        # Delete the income from the month's income list
                        month_data["income"].remove(income)
                        # Update the total income for the month and year
                        month_data["totalIncome"] -= income["price"]
                        year_data["totalIncome"] -= income["price"]
                        # Exit the loop once the income is found and deleted
                        break

        return self._save_expenses(chatID, data)

    def set_expenses(self, chatID, expenses):
        self._save_expenses(chatID, expenses)

    def get_expenses_by_month(self, chatID, date):
        expenses = self.load_json(self._get_filename(chatID))
        
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        year = date.year
        month = date.month


        for y in expenses['years']:
            if y['year'] == year:
                for m in y['months']:
                    if m['month'] == month:
                        return m['expenses']
                break

        return []

    def get_incomes_by_month(self, chatID, date):
        expenses = self.load_json(self._get_filename(chatID))
        
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        year = date.year
        month = date.month

        for y in expenses['years']:
            if y['year'] == year:
                for m in y['months']:
                    if m['month'] == month:
                        return m['income']
                break

        return []

    def get_all_expenses(self, chatID):
        return self.load_json(self._get_filename(chatID))

    def _get_filename(self, chatID):
        users_manager = UsersManager(self.mode)
        return users_manager.get_user_expenses_file(chatID)

    def _save_expenses(self, chatID, expenses):
        
        filename = self._get_filename(chatID)
        with open(filename, "r+") as file:
            file.seek(0)
            json.dump(expenses, file, indent=4, cls=DecimalEncoder)
            file.truncate()    
        return True
