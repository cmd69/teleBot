from classes import Expense, User, AbstractCRUD, AbstractUser
from remodel import DataSource, DataSourceDecorator, SQLDataSource, Controller
from decorators import SheetsDecorator, SheetsDecoratorInterface
import sqlite3



# def client_code(component: DataSource) -> None:
#     """
#     The client code works with all objects using the Component interface. This
#     way it can stay independent of the concrete classes of components it works
#     with.
#     """
#     expense = Expense(1, "2021-01-01", 100, 1, 1, "description")

#     print(f"RESULT: {component.create(expense)}", end="\n\n")
#     print(f"RESULT: {component.get_expenses_by_month()}", end="\n\n")
#     print(f"RESULT: {component.create_curr_month_sheet()}", end="\n\n")

if __name__ == "__main__":

    sql_base = SQLDataSource()
    print("Client: I've got a complex component:", sql_base)
    # client_code(sql_base)
    print("\n")


    sheets_decorator = SheetsDecorator(sql_base)
    print("Client: Now I've got a decorated component:", sheets_decorator.create(Expense(1, "2021-01-01", 100, 1, 1, "description")))
    # client_code(sheets_decorator)

    controller = Controller()

    my_user = User(2100)
    my_expense = Expense(1, "2021-01-01", 100, 1, 1, "description")

    controller.create_expense(my_expense, my_user)




    ### SQL ###

    # conn = sqlite3.connect('./database/sqlite/sqlite.db')
    # cursor = conn.cursor()

    # cursor.execute("SELECT * FROM Category")
    # # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # results = cursor.fetchall()

    # # Print the results
    # print(results)
    # print(type(results))
    # print(type(results[0]))
    # for row in results:
    #     print(row)

    # # Close the cursor and the connection
    # cursor.close()
    # conn.close()