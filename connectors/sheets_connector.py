# Local
from utils import DecimalEncoder
from connectors import AbstractConnector
from classes import AbstractUser, SingletonMeta
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


## Create a class SheetsConnector(Singleton): class that creates a gsheets connection and has a process query method
class SheetsConnector(AbstractConnector):
    def __init__(self):
        super().__init__()
        self.connections_cache = {}

    def _get_credentials(self, user):
        scopes = [os.environ.get('SCOPES')]
        credentials = service_account.Credentials.from_service_account_file(
            user.credentials_path, scopes=scopes)
        return credentials

    def connect(self, user: AbstractUser):
        """
        Establece una conexión con Google Sheets API para un usuario dado y retorna el objeto de servicio.
        """
        # if user.credentials_path not in self.connections_cache:
        #     credentials = self._get_credentials(user)
        #     service = build('sheets', 'v4', credentials=credentials)
        #     self.connections_cache[user.credentials_path] = service
        # return self.connections_cache[user.credentials_path]
        print("Connected to the Google Sheets API")
        return "Connected to the Google Sheets API"


    # def execute(self, user, spreadsheet_id, range_name, operation, values=None):
    def execute(self, user: AbstractUser, query):
        """
        Ejecuta una operación en la hoja de cálculo especificada.
        operation: 'read' o 'write'
        values: necesario si operation es 'write'
        """
        # service = self.connect(user)
        # sheet = service.spreadsheets()

        # if operation == 'read':
        #     result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        #     rows = result.get('values', [])
        #     return rows
        # elif operation == 'write':
        #     body = {
        #         'values': values
        #     }
        #     result = sheet.values().update(
        #         spreadsheetId=spreadsheet_id, range=range_name,
        #         valueInputOption='USER_ENTERED', body=body).execute()
        #     return result
        self.connect(user)
        print("Connected to the Google Sheets API")
        return "Connected to the Google Sheets API"