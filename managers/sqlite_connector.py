# Local
from utils import DecimalEncoder

# Libraries
import json
import decimal
import datetime


class SqliteConnector:
    def __init__(self, mode, users_manager):
        self.users_manager = users_manager

    def add(self, chatID, obj):
        pass

    def get(self, chatID, obj):
        pass

    def mod(self, chatID, obj):
        pass

    def delete(self, chatID, obj):
        pass