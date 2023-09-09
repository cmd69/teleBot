import math
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class KeyboardsGenerator:
    def __init__(self, users_manager) -> None:
        self.users_manager = users_manager
        self.portfolio_buttons = {
            "income": "Ingreso",
            "expense": "Gasto",
            "fetch": "Consultar",
            "deleteExpense": "Eliminar Gasto",
            "back": "Atras ↩️"
        }
        self.benz_buttons = {
            "ride": "Nuevo Recorrido",
            "fill": "Llenar Depósito",
            "fetchBenz": "Consultar",
            "back": "Atras ↩️"
        }
        self.fetch_data_buttons = {
            "general": "General",
            "currMonth": "Este Mes",
            "lastMonth": "Mes Pasado",
            "customMonth": "Otro Mes",
            "back": "Atras ↩️"
        }
        self.settings_buttons = {
            "exit_demo": "Salir del modo demo",
            "back": "Atras ↩️"
            #"enter_demo": "Cargar datos prueba"
        }



    def get_default_keyboards(self):
        ikPortfolio = InlineKeyboardMarkup(row_width=3)
        ikFetchData = InlineKeyboardMarkup(row_width=3)
        ikBenz = InlineKeyboardMarkup(row_width=3)
        ikSettings = InlineKeyboardMarkup(row_width=3)
        mkDescription = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Null'), KeyboardButton('Cancel❌'))
        ikCancel = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
        ikNumeric = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("1€", "2€", "5€", "10€", "20€", "50€", KeyboardButton('Cancel❌'))
        ikMain = InlineKeyboardMarkup().add(
           InlineKeyboardButton(text="Portfolio 📊", callback_data="portfolio"),
           InlineKeyboardButton(text="Settings ⚙️", callback_data="settings")
        )

        ikGuest = InlineKeyboardMarkup().add(
           InlineKeyboardButton(text="Comenzar de cero :)", callback_data="new_user"),
           InlineKeyboardButton(text="Probar demo", callback_data="new_demo")
        )

        for key, value in self.portfolio_buttons.items():
            button = InlineKeyboardButton(text=value, callback_data=key)
            ikPortfolio.insert(button)

        # Create buttons for ikFetchData
        for key, value in self.fetch_data_buttons.items():
            button = InlineKeyboardButton(text=value, callback_data=key)
            ikFetchData.insert(button)

        # Create buttons for ikBenz
        for key, value in self.benz_buttons.items():
            button = InlineKeyboardButton(text=value, callback_data=key)
            ikBenz.insert(button)

        # Create buttons for Settings
        for key, value in self.settings_buttons.items():
            button = InlineKeyboardButton(text=value, callback_data=key)
            ikSettings.insert(button)

        return ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest, ikSettings




    # Create any paginator
    def paginatorFactory(self, chatID, page, gridSize, footerCommand, callbackCommand, expenses):
        
        elements = self.users_manager.get_user_categories(chatID)

        size = len(elements)
        if (not expenses): size+=1

        paginator = InlineKeyboardPaginator(
            math.ceil(size/gridSize),
            current_page=page,
            data_pattern='/'+ footerCommand + '#{page}'
        )
        
        for i in range((page-1)*gridSize, page*gridSize, gridSize):
            list = []

            for c in range(i, i+gridSize):
                if (c >= len(elements)):
                    cat = ""
                else:
                    if (expenses):
                        cat = elements[c][0] + " " + elements[c][1] + " " + elements[c][2] + " " + elements[c][3]  
                    else:
                        cat = elements[c]
                if(not expenses):
                    list.append(InlineKeyboardButton(text=cat, callback_data='/{}#{}'.format(callbackCommand, cat)))
                else:
                    list.append(InlineKeyboardButton(text=cat, callback_data='/{}#{}'.format(callbackCommand, c)))

            if (page == 1 and not expenses): 
                list.insert(0, InlineKeyboardButton(text="Todas✅", callback_data='/{}#{}'.format(callbackCommand, "Todas✅")))

            if (expenses):
                for but in list:
                    paginator.add_before(but)
            else:
                paginator.add_before(list[0], list[1], list[2])
                paginator.add_before(list[3], list[4], list[5])
                paginator.add_before(list[6], list[7], list[8])
        return paginator


    def getCategoriesKeyboard(self, chatID):
    
        ikCategories = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for elem in self.users_manager.get_user_categories(chatID):
            ikCategories.insert(KeyboardButton(elem))
        
        ikCategories.add(KeyboardButton('Cancel❌'))
        return ikCategories


    # Creates Markup or Inline Keyboard. Callback Arg only for
    # Inline Keyboards
    def getSubcategoriesKeyboard(self, chatID, parentCategoryID, markup, callback):
    
        data = self.users_manager.get_all_user_categories(chatID)
              
        if (markup):
            ikSubCategories = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            
            for elem in data:
                category = elem["category"]

                if (category.rstrip(category[-1]) == parentCategoryID
                    and elem["subcategories"] != []):
                    
                    for subcat in elem["subcategories"]:
                        ikSubCategories.insert(KeyboardButton(subcat))            
                        
                    ikSubCategories.add(KeyboardButton('Otro🧭'), KeyboardButton('Cancel❌'))
                    return ikSubCategories
        else:
            ikSubCategories = InlineKeyboardMarkup()
            for elem in data:
                category = elem["category"]
                if (category.rstrip(category[-1]) == parentCategoryID
                    and elem["subcategories"] != []):
                    
                    ikSubCategories.insert(InlineKeyboardButton("Todas🌎", callback_data="/{}#{}".format(callback, "Todas🌎")))
                    for subcat in elem["subcategories"]:
                        n = InlineKeyboardButton(text=subcat, callback_data="/{}#{}".format(callback, subcat))
                        ikSubCategories.insert(n)
                    
                    ikSubCategories.insert(InlineKeyboardButton(text="Cancelar❌", callback_data="cancel"))
                    return ikSubCategories
        return False



