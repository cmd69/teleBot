import sqlite3
from classes.Singleton import Singleton

class SqliteConnector(Singleton):
    def __init__(self):
        self.connection = None

    def connect(self):
        # Connect to the SQLite database
        # self.connection = sqlite3.connect('database.db')
        return "Connected to the SQLite database"
