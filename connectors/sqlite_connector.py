import sqlite3
from classes import AbstractUser, SingletonMeta
from connectors import AbstractConnector


class SqliteConnector(AbstractConnector):
    def __init__(self):
        self.connection = None

    def connect(self):
        # Connect to the SQLite database
        # self.connection = sqlite3.connect('database.db')
        print("Connected to the SQLite database")
        return "Connected to the SQLite database"
    
    def execute(self, user: AbstractUser, query):
        self.connect()
        print(f"Executing query: {query}")
        return "Executing query: "
