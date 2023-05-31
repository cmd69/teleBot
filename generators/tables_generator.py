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
        incomes_table.field_names = ["Date 📅", "Descript. 🔰", "Price 💸"]
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
        formatted_table = f"\n\n{incomes_table}\n\n{expenses_table}\n\n \nIncome: {round(total_income,2)} € \nExpenses: {round(total_expenses,2)} €\nSaved: {round(remaining,2)} €"
        
        return formatted_table

    
    def generate_general_report(self, expenses):

        recap_message = "💰 Budget Recap 💰\n\n"
        
        years = expenses["years"]
        total_income = 0
        total_expenses = 0
        total_saved = 0
        total_income_count = 0
        total_expenses_count = 0
        
        for year_data in years:
            months = year_data["months"]
            
            for month_data in months:
                expenses = month_data["expenses"]
                income = month_data["income"]
                
                if income:
                    total_income += sum(entry['price'] for entry in income)
                    total_income_count += len(income)
                
                if expenses:
                    total_expenses += sum(entry['price'] for entry in expenses)
                    total_expenses_count += len(expenses)
        

        # Calculate average expenses
        if total_expenses_count > 0:
            average_expenses = total_expenses / total_expenses_count
            percentage_of_expenses = (average_expenses / total_income) * 100
            recap_message += f"💸 Avg. Expenses: €{average_expenses:.2f} ({percentage_of_expenses:.2f}%)\n"
        
        
        if total_income_count > 0:
            # Calculate average income    
            average_income = total_income / total_income_count
            recap_message += f"💵 Avg. Income: €{average_income:.2f}\n"

            # Calculate average saved
            average_saved = average_income - average_expenses
            recap_message += f"💰 Avg. Saved: €{average_saved:.2f} ({(average_saved / total_income) * 100:.2f}%)\n\n"
        else:
            recap_message += f"💵 Avg. Income: €{total_income_count:.2f}\n"
            recap_message += f"💰 Avg. Saved: €{total_income_count:.2f} ({(total_income_count) * 100:.2f}%)\n\n"
        
        
        

        
        # Calculate average category expenses
        all_expenses = [entry for year_data in years for month_data in year_data["months"] for entry in month_data["expenses"]]
        categories = {}
        total_expenses = 0
        
        for expense in all_expenses:
            category = expense["category"]
            price = expense["price"]
            total_expenses += price
            
            if category in categories:
                categories[category]["total"] += price
                categories[category]["count"] += 1
            else:
                categories[category] = {"total": price, "count": 1}
        
        recap_message += "📊 Category Averages\n"
        
        # Create the pretty table
        table = pt.PrettyTable()
        table.field_names = ["Category", "Avg (€)", "(%)"]
        
        for category, data in categories.items():
            average_expense = data["total"] / data["count"]
            percentage_of_expenses = (data["total"] / total_expenses) * 100
            table.add_row([category, f"€{average_expense:.2f}", f"{percentage_of_expenses:.2f}"])
        
        recap_message += str(table)
        
        return recap_message


