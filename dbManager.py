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

    return jsonManager.add_expense(mode, chatID, year, month, expense)
    

def newExpenseSheets():
    pass

def getMonthExpensesJson():
    pass

def getMonthExpensesSheets():
    pass

