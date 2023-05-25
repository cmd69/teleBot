import datetime
import json
import jsonManager
import sheetsManager

def newExpenseJson(mode, chatID, expense):
    # Extract the date from the object
    date_str = expense.get('date')

    # Split the date string into day, month, and year
    day, month, year = date_str.split('/')

    # Convert day and year to integers
    day = int(day)
    month = int(month)
    year = int(year)

    return jsonManager.addExpense(mode, chatID, year, month, expense)


def newIncomeJson(mode, chatID, income):
    return jsonManager.newIncomeJson(mode, chatID, income)

def getAllExpensesJson(mode, chatID):
    return jsonManager.getExpenses(mode, chatID)
    
def getMonthExpensesJson(mode, chatID, consult):
    
    # Example of consult object
    # consult = {
    #     'date': date,
    #     'category': category,
    #     'subcategory': subcategory
    # }

    date_str = consult.get('date')

    # Split the date string into day, month, and year
    day, month, year = date_str.split('/')
    subcategory = consult.get('subcategory')
    category = consult.get('category')
    # Convert month and year to integers
    month = int(month)
    year = int(year)

    expenses, tIncome, tExpenses = jsonManager.get_expenses(mode, chatID, year, month)

    filtered_expenses = filterExpenses(expenses, category, subcategory)
    return filtered_expenses, tIncome, tExpenses
    

def newExpenseSheets():
    pass



def getMonthExpensesSheets(chatID, consult):
    
    date_str = consult.get('date')
    category = consult.get('category')
    subcategory = consult.get('subcategory')

    # Split the date string into day, month, and year
    day, month, year = date_str.split('/')
    # Convert month and year to integers
    month = int(month)
    year = int(year)
    
    expenses = sheetsManager.getMonthExpenses(chatID, date_str)
    
    expenses_clean = sheetsToJson(expenses)
    filtered_expenses = filterExpenses(expenses_clean, category, subcategory)
    return filtered_expenses
    # return filtered_expenses


# ╔═══════════════════╗
# |||  AUX METHODS  |||
# ╚═══════════════════╝

def sheetsToJson(data):

    def convert_xls_datetime(xls_date):
        return (datetime.datetime(1899, 12, 30)
                + datetime.timedelta(days=xls_date))

    json_objects = []
    for item in data:
        
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

def sumExpenses():
    pass

def filterExpenses(expenses, category, subcategory):

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



# def getSubcategories(chatID, category):

#     list = []
#     categories = getUserCategories(chatID)
    
#     for elem in categories:
#         cat = elem["category"].rstrip(elem["category"][-1:])

#     return list