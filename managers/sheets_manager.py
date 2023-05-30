from __future__ import print_function
import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from dotenv import load_dotenv

# from UsersManager import UsersManager

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


class SheetsManager:
    def __init__(self, mode, users_manager):
        self.mode = mode
        self.users_manager = users_manager
        self.users_portfolios = {}

    def _get_credentials(self, chatID):
        creds_file = self.users_manager.get_user_creds(chatID)
        credentials =  service_account.Credentials.from_service_account_file(creds_file, scopes=[os.environ.get('SCOPES')])
        return credentials

    def _load_user_portfolio(self, chatID):
        if chatID not in self.users_portfolios:
            credentials = self._get_credentials(chatID)
            service = build('sheets', 'v4', credentials=credentials)
            portfolio = service.spreadsheets()

            self.users_portfolios[chatID] = portfolio
        
        return self.users_portfolios[chatID]



    def _get_portfolio_sheet(self, chatID):
        return self.users_manager.get_user_sheetsFile(chatID)

    def _get_date_format(self, chatID):
        return self.users_manager.get_user_date_format(chatID)


    def add_expense(self, chatID, expense):

        date = expense['date']
        category = expense['category']
        price = expense['price']
        description = expense['description']
        
        if (expense['subcategory'] != None): 
            subcategory = expense['subcategory']
        else: 
            subcategory = expense['category']
        

        # Sheet corresponding to the months expense
        dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B9:F"
        
        if (self._get_date_format(chatID) == "mmddyy"):
            date_obj = datetime.datetime.strptime(date, '%d/%m/%Y')
            date = date_obj.strftime('%m/%d/%Y')

        # Expense array creation
        expense = [[date, category, subcategory, price, description]]        

        try:
            request = self._load_user_portfolio(chatID).values().append(
                    spreadsheetId=self._get_portfolio_sheet(chatID),
                    range = sheet,
                    valueInputOption="USER_ENTERED",
                    # insertDataOption="INSERT_ROWS",
                    body={"values":expense}).execute()
            print('Nueva transacción: ' + self.users_manager.get_user_name(self.mode, chatID) + " --> " + str(expense))
            return True

        except HttpError as error:
            print(str(error))
            return False
        
    def add_income(self, chatID, income):
        date = income['date']
        price = income['price']
        description = income['description']


        # Sheet corresponding to the months expense
        dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!S9:U"
        
        # Adjust date depending on shpreadsheet's date preferences
        if (self._get_date_format(chatID) == "mmddyy"):
                date2 = datetime.datetime.strptime(date, "%d/%m/%Y")
                date = str(date2.month) + '/' + str(date2.day) + '/' + str(date2.year)

        # Expense array creation
        expense = [[date, price, description]]        

        try:
            request = self._load_user_portfolio(chatID).values().append(
                    spreadsheetId=self._get_portfolio_sheet(chatID),
                    range = sheet,
                    valueInputOption="USER_ENTERED",
                    # insertDataOption="INSERT_ROWS",
                    body={"values":expense}).execute()
            print('Nueva transacción: ' + self.users_manager.get_user_name(chatID) + " --> " + str(expense))
            return True

        except HttpError as error:
                print(str(error))

    def delete_expense(self, chatID, index):

        # portfolio = loadPortfolio(chatID)
        # credentials, sheetsFile = usersManager.getUserData(chatID)
        # dateFormat = usersManager.getUserDateFormat(chatID)

        # # Sheet corresponding to the months expense
        # dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        # deleteRange = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B" + str(10+int(index)) + ":E" + str(10+int(index))
        
        # # Adjust date depending on shpreadsheet's date preferences
        # if (dateFormat == "mmddyy"):
        #         date2 = datetime.datetime.strptime(date, "%d/%m/%Y")
        #         date = str(date2.month) + '/' + str(date2.day) + '/' + str(date2.year)
        
        # try:
        #         res = portfolio.values().clear(spreadsheetId=sheetsFile, range=deleteRange).execute()
        #         return True
        # except HttpError as error:
        #         print(str(error))
        pass

    def delete_income(self, chatID, income):
        incomes_sheet = self._get_portfolio_sheet(chatID)
        pass

    def get_all_expenses(self, chatID):
        # expenses_sheet = self._get_portfolio_sheet()
        pass

    def get_expenses_by_month(self, chatID, date):
        try:
            dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        except:
            print("sheetsManager.getMonthExpenses: strptime except")
            dateClass = date
        
        sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!B10:F"
        
        result = self._load_user_portfolio(chatID).values().get(spreadsheetId=self._get_portfolio_sheet(chatID),
                                valueRenderOption="UNFORMATTED_VALUE",
                                range=sheet).execute()
        
        expenses = result.get('values', [])
        
        return expenses

    def get_incomes_by_month(self, chatId, date):
        # portfolio = loadPortfolio(chatID)
        # credentials, sheetsFile = usersManager.getUserData(mode, chatID)

        # try:
        #         dateClass = datetime.datetime.strptime(date, "%d/%m/%Y")
        # except:
        #         print("sheetsManager.getMonthExpenses: strptime except")
        #         dateClass = date
        
        # sheet = months[str(dateClass.month)] + str(dateClass.year)[-2:] + "!S10:U"
        
        # result = portfolio.values().get(spreadsheetId=sheetsFile,
        #                         valueRenderOption="UNFORMATTED_VALUE",
        #                         range=sheet).execute()
        
        # expenses = result.get('values', [])
        # print(expenses)
        # return expenses

        pass