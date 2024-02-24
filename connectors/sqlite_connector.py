import sqlite3
from classes import AbstractUser, SingletonMeta
from connectors import AbstractConnector
import os
from dotenv import load_dotenv


class SqliteConnector(AbstractConnector):
    def __init__(self):
        self.connection = None

    def connect(self):
        
        if self.connection is not None:
            return self.connection

        load_dotenv()
        db_path = os.getenv('DEV_SQLITE3')
        print(f"Connecting to SQLite database at {db_path}")
        if db_path is None:
            raise ValueError("DB_PATH is not specified in the .env file")

        self.connection = sqlite3.connect(db_path)
        return self.connection
    
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    def execute(self, user, query, values=None):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            
            print(f"Executing query: {query} on user: {user}")
            cursor.execute(query, values) if values is not None else cursor.execute(query)
            
            if query.lower().startswith(("insert", "update", "delete")):
                connection.commit()
            return cursor
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
        finally:
            cursor.close()
