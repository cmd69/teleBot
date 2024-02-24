from classes import Expense, User, AbstractCRUD, AbstractUser
from remodel import DataSource, DataSourceDecorator, SQLDataSource, Controller
from decorators import SheetsDecorator, SheetsDecoratorInterface
import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv
from datetime import date as Date

def create_connection(db_file):
    """Create a database connection to a SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite. SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    load_dotenv
    database = os.getenv('DEV_SQLITE3')
    print(f"Connecting to SQLite database at {database}")
    database = database + "/test1.db"
    print(f"Connecting to SQLite database at {database}")

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        chat_id integer PRIMARY KEY,
                                        username text NOT NULL
                                    ); """

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        create_table(conn, sql_create_users_table)
        print("Table 'users' created successfully.")
    else:
        print("Error! Cannot create the database connection.")

    # Close the connection
    if conn:
        conn.close()


if __name__ == "__main__":

    # sql_base = SQLDataSource()

    controller = Controller()

    my_user = User(256900373, "Altoke")
    my_expense = Expense(1, "2021-01-01", 100, "description")

    # connection = sqlite3.connect('./database/sqlite/sqlite.db')

    # a = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER';")
    # print(a.fetchall())
    date = Date(2021, 1, 1)
    result = controller.get_month_transactions(my_user, my_expense, date)
    print("Result: ", result)

    
    ### SQL ###

    # main()


    



