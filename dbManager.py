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
    
def getMonthExpensesJson(mode, chatID, consult):

    date_str = consult.get('date')

    # Split the date string into day, month, and year
    day, month, year = date_str.split('/')

    # Convert month and year to integers
    month = int(month)
    year = int(year)

    return jsonManager.get_expenses(mode, chatID, year, month)
    

def newExpenseSheets():
    pass



def getMonthExpensesSheets():
    pass


# ╔═══════════════════╗
# |||  AUX METHODS  |||
# ╚═══════════════════╝


def filterExpenses():
    pass

def sumExpenses():
    pass