import prettytable as pt


class TableGenerator:
    def __init__(self, users_manager):
        self.users_manager = users_manager

    def generate_month_recap(self, consult, expenses):
    
        table = pt.PrettyTable(['📅', '🔰', '💸'])
        table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]

        category = consult['category']
        subcategory = consult['subcategory']
        
        total_expenses = 0

        # 1 Mostrar TODOS los gastos
        # 2 Mostrar subcategorias de una categoria
        if (category == "Todas"):
            table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]
            # Add rows to the table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                cat = expense['category']
                price = expense['price']
                table.add_row([day, cat, f"${price}"])
                total_expenses += round(float(price), 2)
        elif subcategory == None or subcategory == "Todas":
            table.field_names = ["Date 📅", "Subcat. 🗓️", "Price 💸"]
            # Add rows to the table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                subcat = expense['subcategory']
                price = expense['price']
                table.add_row([day, subcat, f"${price}"])
                total_expenses += price
        else:
            table.field_names = ["Date 📅", "Desc. 🗓️", "Price 💸"]
            # Add rows to the table and calculate total expenses
            for expense in expenses:
                day = expense['date'].split('/')[0]
                description = expense['description']
                price = expense['price']
                table.add_row([day, description, f"${price}"])
                total_expenses += price

        # Calculate remaining amount
        tIncome = 12345
        remaining = tIncome - total_expenses

        table.align = "l"
        table.padding_width = 1
        table.format = True

        # Create a string with the formatted table
        formatted_table = f"\n\n{table}\n\n \nIncome: {round(tIncome,2)} € \nExpenses: {round(total_expenses,2)} €\nSaved: {round(remaining,2)} €"

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
        
        # Calculate average income
        if total_income_count > 0:
            average_income = total_income / total_income_count
            recap_message += f"💵 Avg. Income: €{average_income:.2f}\n"
        
        # Calculate average expenses
        if total_expenses_count > 0:
            average_expenses = total_expenses / total_expenses_count
            percentage_of_expenses = (average_expenses / total_income) * 100
            recap_message += f"💸 Avg. Expenses: €{average_expenses:.2f} ({percentage_of_expenses:.2f}%)\n"
        
        # Calculate average saved
        average_saved = average_income - average_expenses
        recap_message += f"💰 Avg. Saved: €{average_saved:.2f} ({(average_saved / total_income) * 100:.2f}%)\n\n"
        
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


