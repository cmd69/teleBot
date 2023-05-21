import os
from dotenv import load_dotenv
from flask import Flask
import dbManager
import jsonManager
import threading
import asyncio


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

# Local Imports

## Import the button dictionaries from separate files
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.keyboards.portfolio_keyboard import portfolio_buttons
from database.keyboards.fetch_data_keyboard import fetch_data_buttons
from database.keyboards.benz_keyboard import benz_buttons
from aiogram.dispatcher.filters.state import State, StatesGroup


# ╔═════════════════════╗
# ||| INITIALIZATIONS |||
# ╚═════════════════════╝


#
# ----- Flask Setup ----- #
#
app = Flask(__name__)
mode = os.environ.get('TELEBOT_ENV', 'development')  # Default to development mode if not specified

if mode == 'production':
    app.config.from_pyfile('settings/configProd.py')
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False})
else:
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False})
    app.config.from_pyfile('settings/configDev.py')


flask_thread.start()

# Start the Telegram bot using the aiogram executor

#
# ----- Bot Setup ----- #
#
bot = Bot(token=app.config["BOT_TOKEN"])
storage = MemoryStorage()  # external storage is supported!
dp = Dispatcher(bot, storage=storage)



#
# ----- Keyboards Setup ----- #
#
benz_buttons = {
    "ride": "Nuevo Recorrido",
    "fill": "Llenar Depósito",
    "fetchBenz": "Consultar",
    "back": "Atras ↩️"
}

fetch_data_buttons = {
    "general": "General",
    "currMonth": "Este Mes",
    "lastMonth": "Mes Pasado",
    "customMonth": "Otro Mes",
    "back": "Atras ↩️"
}

portfolio_buttons = {
    "income": "Ingreso",
    "expense": "Gasto",
    "fetch": "Consultar",
    "deleteExpense": "Eliminar Gasto",
    "back": "Atras ↩️"
}

# Create InlineKeyboardMarkup for each dictionary
ikPortfolio = InlineKeyboardMarkup(row_width=3)
ikFetchData = InlineKeyboardMarkup(row_width=3)
ikBenz = InlineKeyboardMarkup(row_width=3)


# Create buttons for ikMain
ib1 = InlineKeyboardButton(text="Portfolio 📊", callback_data="portfolio")
ib2 = InlineKeyboardButton(text="Benz 🚓", callback_data="benz")
ikMain = InlineKeyboardMarkup().add(ib1, ib2)

# Create buttons for ikPortfolio
for key, value in portfolio_buttons.items():
    button = InlineKeyboardButton(text=value, callback_data=key)
    ikPortfolio.insert(button)

# Create buttons for ikFetchData
for key, value in fetch_data_buttons.items():
    button = InlineKeyboardButton(text=value, callback_data=key)
    ikFetchData.insert(button)

# Create buttons for ikBenz
for key, value in benz_buttons.items():
    button = InlineKeyboardButton(text=value, callback_data=key)
    ikBenz.insert(button)



#
# ----- States Setup ----- #
#
class Expense(StatesGroup):
    category = State()
    subcategory = State()
    price = State()
    date = State()
    description = State()

class NewIncome(StatesGroup):
    amount = State()

class FetchFilters(StatesGroup):
    date = State()
    filter = State()
    category = State()
    subcategory = State()

class ConsultMonth1(StatesGroup):
    date = State()

class ConsultMonth2(StatesGroup):
    date = State()
    expense = State()

class Fill(StatesGroup):
    price = State()
    diesel = State()
    date = State()




# /Start and /Help
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Hola, bienvenido a tu gestor de portfolio!", reply_markup=ikMain)

# Main Menu
@dp.callback_query_handler(text = ["portfolio", "benz"])
async def random_value(call: types.CallbackQuery):
    
    chatID = call.message.chat.id
    messageID = call.message.message_id

    # if (dbManager.userExists(call.message.chat.id)):
    if (jsonManager.getMonthExpenses(app.config["MODE"], chatID)):
        
        print(jsonManager.getMonthExpenses(app.config["MODE"], chatID))
        if call.data == "portfolio":
            
            await bot.edit_message_reply_markup(
                                    chatID,
                                    messageID,
                                    inline_message_id= None,
                                    reply_markup=ikPortfolio)
        if call.data =="benz":
            
            await bot.edit_message_text("Mostrando menu de opciones... ",
                                    chatID,
                                    messageID)
            
            await bot.edit_message_reply_markup(
                                    chatID,
                                    messageID,
                                    inline_message_id= None,
                                    reply_markup=ikBenz)
        await call.answer()    
    else:
        
        await call.message.answer("No tienes acceso a este servicio")   


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
