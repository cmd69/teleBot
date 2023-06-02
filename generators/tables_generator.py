import prettytable as pt


class TableGenerator:
    def __init__(self, users_manager):
        self.users_manager = users_manager

    def generate_month_recap(self, consult, expenses, incomes):
    
        # Expenses Table
        expenses_table = pt.PrettyTable(['📅', '🔰', '💸'])
        expenses_table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]
        expenses_table.align = "l"
        expenses_table.padding_width = 1
        expenses_table.format = True


        # Incomes table
        incomes_table = pt.PrettyTable(['📅', '🔰', '💸'])
        incomes_table.field_names = ["Date 📅", "Desc. 🔰", "Price 💸"]
        incomes_table.align = "l"
        incomes_table.padding_width = 1
        incomes_table.format = True

        
        
        # FILL EXPENSES TABLE
        total_expenses = 0
        category = consult['category']
        subcategory = consult['subcategory']

        # 1 Mostrar TODOS los gastos
        # 2 Mostrar subcategorias de una categoria
        if (category == "Todas"):
            expenses_table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]
            # Add rows to the expenses_table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                cat = expense['category']
                price = expense['price']
                expenses_table.add_row([day, cat, f"${price}"])
                total_expenses += round(float(price), 2)
        elif subcategory == None or subcategory == "Todas":
            expenses_table.field_names = ["Date 📅", "Subcat. 🗓️", "Price 💸"]
            # Add rows to the expenses_table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                subcat = expense['subcategory']
                price = expense['price']
                expenses_table.add_row([day, subcat, f"${price}"])
                total_expenses += price
        else:
            expenses_table.field_names = ["Date 📅", "Desc. 🗓️", "Price 💸"]
            # Add rows to the expenses_table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                description = expense['description']
                price = expense['price']
                expenses_table.add_row([day, description, f"${price}"])
                total_expenses += price

        
        
        
        # FILL INCOMES TABLE
        total_income = 0

        # Add rows to the expenses_table and calculate total expenses
        for income in incomes:
            day = income['date'].split('/')[0]
            description = income['description']
            price = income['price']
            incomes_table.add_row([day, description, f"${price}"])
            total_income += price

        # Calculate remaining amount
        
        remaining = total_income - total_expenses

        # Create a string with the formatted expenses_table
        formatted_table = f"\n\n\nINGRESOS:\n{incomes_table}\n\nGASTOS\n{expenses_table}\n\n \nIncome: {round(total_income,2)} € \nExpenses: {round(total_expenses,2)} €\nSaved: {round(remaining,2)} €"
        
        return formatted_table


    def generate_general_report(self, expenses):
        recap_message = "💰 Budget Recap 💰\n\n"
        
        years = expenses["years"]
        total_income_count = 0
        total_expenses_count = 0

        number_months = 0

        for year_data in years:
            months = year_data["months"]
            
            for month_data in months:
                
                expenses_list = month_data["expenses"]
                income_list = month_data["income"]
                
                if income_list or expenses_list:
                    number_months += 1

                if income_list:
                    total_income_count += month_data["totalIncome"]
                
                if expenses_list:
                    total_expenses_count += month_data["totalExpenses"]


        # Calculate average income
        if total_income_count > 0 and number_months > 0:
            average_income = total_income_count / number_months
            recap_message += f"💵 Avg. Income: €{average_income:.2f}\n"
        else:
            average_income = 0
            recap_message += "💵 Avg. Income: €0.00\n"

        # Calculate average expenses
        if total_expenses_count > 0 and number_months > 0:
            average_expenses = total_expenses_count / number_months
            if total_income_count > 0:
                percentage_of_expenses = (average_expenses / average_income) * 100
            else:
                percentage_of_expenses = 0
            recap_message += f"💸 Avg. Expenses: €{average_expenses:.2f} ({percentage_of_expenses:.2f}%)\n"
        else:
            average_expenses = 0
            percentage_of_expenses = 0
            recap_message += "💸 Avg. Expenses: €0.00 (0.00%)\n"

        # Calculate average saved
        average_saved = average_income - average_expenses
        if total_income_count > 0:
            recap_message += f"💰 Avg. Saved: €{average_saved:.2f} ({(average_saved / average_income) * 100:.2f}%)\n\n"
        else:
            recap_message += f"💰 Avg. Saved: €{average_saved:.2f} ({0 * 100:.2f}%)\n\n"


        
        categories = {}  # Dictionary to store category-wise expenses

        # Iterate over the years and months in the expenses JSON
        for year in expenses['years']:
            for month in year['months']:
                for expense in month['expenses']:
                    category = expense['category']
                    price = expense['price']
                    if category in categories:
                        categories[category]['total'] += price
                    else:
                        categories[category] = {'total': price}

        
        # Create a pretty table
        table = pt.PrettyTable(['Category', '€', '%'])

        # Calculate average expense and percentage for each category
        for category, data in categories.items():
            average_expense = data['total'] / number_months
            expense_percentage = (average_expense / average_income) * 100 
            table.add_row([category, str(round(average_expense, 2)) + " €", str(round(expense_percentage, 1)) + " %"])
        
        recap_message += str(table)
        
        return recap_message
