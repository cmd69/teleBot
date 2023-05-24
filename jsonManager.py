import os
import os.path
import json
import datetime
import sheetsManager
import logging
import usersManager
import functools
from flask_caching import Cache

from dotenv import load_dotenv

load_dotenv()

# ╔═══════════════════╗
# |||    GETTERS    |||
# ╚═══════════════════╝


# cache = Cache()  # Initialize Flask-Caching

def cache_user_data(func):
    user_data_cache = {}

    @functools.wraps(func)
    def wrapper(mode, *args, **kwargs):
        chatID = args[0]
        cache_key = f"{mode}_{chatID}_{func.__name__}"
        
        if cache_key in user_data_cache:
            return user_data_cache[cache_key]
        else:
            result = func(mode, *args, **kwargs)
            user_data_cache[cache_key] = result
            return result

    return wrapper



@cache_user_data
def getExpenses(mode, chatID):
    try:
        expensesFile = usersManager.getUserExpensesFile(mode, chatID)
        with open(expensesFile) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise Exception("Expenses file not found.")
    except (KeyError, ValueError):
        raise Exception("Invalid JSON format in expenses file.")





@cache_user_data
def getMonthExpenses(mode, chatID, date, category, subcategory):
    try:
        datem = datetime.datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        print("jsonManager.getMonthExpenses: strptime except")
        datem = date

    yy = str(datem.year)
    mm = str(datem.month)

    # Assuming sheetsManager is defined elsewhere
    expenses = sheetsManager.getMonthExpenses(chatID, date, category, subcategory)
    
    # expenses = createExpenseObj(expenses)

    # expenses = filterExpenses(chatID, expenses, category, subcategory)
    # total = sumExpenses(expenses)

    return expenses




# ╔═══════════════════╗
# |||  JSON ACCESS  |||
# ╚═══════════════════╝

import decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

        
def addExpense(mode, chatID, year, month, expense):
    try:
        expensesFile = usersManager.getUserExpensesFile(mode, chatID)
    except FileNotFoundError:
        raise Exception("Expenses file not found.")

    with open(expensesFile, 'r+') as file:
        data = json.load(file)
        for y in data['years']:
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
            data['years'].append({
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
        file.seek(0)
        json.dump(data, file, indent=4, cls=DecimalEncoder)
        file.truncate()

def get_expenses(mode, chatID, year, month):
    
    try:
        data = getExpenses(mode, chatID)
    except FileNotFoundError:
        raise Exception("Expenses file not found.")
    
    for y in data['years']:
        if y['year'] == year:
            
            for m in y['months']:
                if m['month'] == month:
                    return m['expenses'], round(float(m['totalIncome']),2), round(float(m['totalExpenses']),2)
            break
    
    return [], 0, 0



# UPDATES JSON WITH SHEETS
# WONT BE NECESSARY
def updateMonthExpenses(chatID, dates):

    for date in dates:
        datem = datetime.datetime.strptime(date, "%d/%m/%Y")
        yy = datem.year
        mm = datem.month

        print("Updating " + datem.strftime("%B") + " expenses...")

        exp = sheetsManager.getMonthExpenses(chatID, date, "Todas", False)
        sheetExpenses = createExpenseObj(exp[0])

        jsonDB = getExpenses(chatID)

        for year in jsonDB:

            id = year.get('year')
            if (str(yy) == id):
                year['months'][str(mm)]['Expenses'] = sheetExpenses
                saveFile(chatID, jsonDB)

    return True



# ADD NEW EXPENSE TO A MONTH

def newExpense(chatID, date, category, subcategory, price, description):

    if (chatID == None or date == None or category == None or price == None):
        return False

    datem = datetime.datetime.strptime(date, "%d/%m/%Y")
    yy = datem.year
    mm = datem.month

    expenses = getExpenses(chatID)

    for year in expenses:
        
        expensesYear = year.get('year')  
        
        if (expensesYear == str(yy)):
            
            # try:
            e = createExpenseObj([[date, category, subcategory, price, description]])
            sheetsManager.newExpense(chatID, e)
            # year['months'][str(mm)]['Expenses'].append(e[0])
            year['months'][str(mm)].append(e[0])
            return saveFile(chatID, expenses)

    return False


def newIncomeJson(mode, chatID, income):

    file = usersManager.getUserExpensesFile(mode, chatID)

    with open(file, 'r+') as file:
        data = json.load(file)
        
        # Find the year and month in the income object
        date_str = income['date']
        day, month, year = map(int, date_str.split('/'))
        
        # Find the year index in the JSON structure
        year_index = None
        for i, year_data in enumerate(data['years']):
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
            data['years'].append(year_data)
            year_index = len(data['years']) - 1
        
        # Find the month index in the year's months list
        month_index = None
        for i, month_data in enumerate(data['years'][year_index]['months']):
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
            data['years'][year_index]['months'].append(month_data)
            month_index = len(data['years'][year_index]['months']) - 1
        
        # Add the new income to the month's income list
        data['years'][year_index]['months'][month_index]['income'].append(income)
        
        # Update the total income for the month, year, and overall
        data['years'][year_index]['months'][month_index]['totalIncome'] += income['price']
        data['years'][year_index]['totalIncome'] += income['price']
        
        # Move the file pointer to the beginning and write the updated JSON
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    
    return True




# ╔═══════════════════╗
# |||  AUX METHODS  |||
# ╚═══════════════════╝



def saveFile(chatID, data):
    try:
        filename = usersManager.getUserExpensesFile(chatID)
        with open(filename, "w") as file:
            json.dump(data, file)
        file.close()
        return True
    except:
        return False

def createExpenseObj(expenses):
    jsonExpenses = []


    def convert_xls_datetime(xls_date):
        return (datetime.datetime(1899, 12, 30)
                + datetime.timedelta(days=xls_date))

    for exp in expenses:

        date = exp[0]
        
        # Cuando recuperamos un gasto de Sheets, la fecha se
        # devuelve en formato int, ej: 778219. Hay que comprobar
        # para hacer la conv. a string, ej: "dd/MM/yy".
        if type(date) == int:
            date = convert_xls_datetime(date)
            date = datetime.datetime.strftime(date, "%d/%m/%Y")
            date = str(date)

        category = exp[1]
        subcategory = exp[2]
        price = exp[3]
        description = exp[4]

        obj = {
            "date": date,
            "category": category,
            "subcategory": subcategory,
            "price": price,
            "description": description
        }
        jsonExpenses.append(obj)

    if (len(expenses) == 1):
        return [obj]
    else:
        return jsonExpenses

def sumExpenses(expenses):

    amount = 0

    if (expenses):
        for exp in expenses:
            amount += float(exp['price'])

    return round(amount, 2)

def filterExpenses(chatID, expenses, category, subcategory):

    filtered = []

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

