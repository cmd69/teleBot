from __future__ import print_function
import os
import usersManager
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

portfolios = {}


months = {
    "1": "JAN",
    "2": "FEB",
    "3": "MAR",
    "4": "APR",
    "5": "MAY",
    "6": "JUN",
    "7": "JUL",
    "8": "AUG",
    "9": "SEPT",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC"
}

# Load or return user portfolio if already exists
def loadPortfolio(chatID):

        if (chatID not in portfolios):
                creds = service_account.Credentials.from_service_account_file(
                    usersManager.getUserCreds(chatID), scopes=os.environ.get('SCOPES'))

                service = build('sheets', 'v4', credentials = creds)

                loadedPortfolio = service.spreadsheets()
                
                portfolios[chatID] = loadedPortfolio

        return portfolios[chatID]




def dateToDDMM(date):
        date2 = datetime.datetime.strptime(date, "%m/%d/%Y")
        date = str(date2.day) + '/' + str(date2.month) + '/' + str(date2.year)
        return date

def dateToMMDD(date):
        date2 = datetime.datetime.strptime(date, "%d/%m/%Y")
        date = str(date2.month) + '/' + str(date2.day) + '/' + str(date2.year)
        return date


def newExpense(chatID, expenses):
        
        portfolio = loadPortfolio(chatID)
        credentials, sheetsFile = usersManager.getUserData(chatID)
        dateFormat = usersManager.getUserDateFormat(chatID)
        
        for exp in expenses:

                date = exp['date']
                category = exp['category']
                if (exp['subcategory'] != None):
                        subcategory = exp['subcategory']
                else:
                        subcategory = exp['category']
                price = exp['price']
                description = exp['description']


                # Sheet corresponding to the months expense
                dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
                sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B9:F"
                
                
                # Adjust date depending on shpreadsheet's date preferences
                if (dateFormat == "mmddyy"):
                        date2 = datetime.datetime.strptime(date, "%d/%m/%Y")
                        date = str(date2.month) + '/' + str(date2.day) + '/' + str(date2.year)

                # Expense array creation
                expense = [[date, category, subcategory, price, description]]        


                try:
                        request = portfolio.values().append(
                                spreadsheetId=sheetsFile,
                                range = sheet,
                                valueInputOption="USER_ENTERED",
                                # insertDataOption="INSERT_ROWS",
                                body={"values":expense}).execute()
                        print('Nueva transacción: ' + usersManager.getUserName(chatID) + " --> " + str(expense))
                        # return True

                except HttpError as error:
                        print(str(error))


def deleteExpense(chatID, date, index):
        
        portfolio = loadPortfolio(chatID)
        credentials, sheetsFile = usersManager.getUserData(chatID)
        dateFormat = usersManager.getUserDateFormat(chatID)

        # Sheet corresponding to the months expense
        dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        deleteRange = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B" + str(10+int(index)) + ":E" + str(10+int(index))
        
        # Adjust date depending on shpreadsheet's date preferences
        if (dateFormat == "mmddyy"):
                date2 = datetime.datetime.strptime(date, "%d/%m/%Y")
                date = str(date2.month) + '/' + str(date2.day) + '/' + str(date2.year)
        
        try:
                res = portfolio.values().clear(spreadsheetId=sheetsFile, range=deleteRange).execute()
                return True
        except HttpError as error:
                print(str(error))
        

def getMonthExpenses(chatID, date, category, subcategory):
        portfolio = loadPortfolio(chatID)
        credentials, sheetsFile = usersManager.getUserData(chatID)
        
        try:
                dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        except:
                print("daoSheets.getMonthExpenses: strptime except")
                dateClass = date
        
        sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B10:F"
        

        result = portfolio.values().get(spreadsheetId=sheetsFile,
                                valueRenderOption="UNFORMATTED_VALUE",
                                range=sheet).execute()
        
        expenses = result.get('values', [])

        return expenses