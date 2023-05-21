import os
from dotenv import load_dotenv
from flask import Flask
import dbManager
import jsonManager
import usersManager
import json
import threading
import asyncio


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

# Local Imports

## Import the button dictionaries from separate files
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from database.keyboards.portfolio_keyboard import portfolio_buttons
from database.keyboards.fetch_data_keyboard import fetch_data_buttons
from database.keyboards.benz_keyboard import benz_buttons
from aiogram.dispatcher.filters.state import State, StatesGroup
import math
import prettytable as pt

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta, datetime

import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


# ╔═════════════════════╗
# ||| INITIALIZATIONS |||
# ╚═════════════════════╝


#
# ----- Flask Setup ----- #
#
app = Flask(__name__)
mode = os.environ.get('TELEBOT_ENV', 'dev')  # Default to development mode if not specified

if mode == 'prod':
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

    if (usersManager.userExists(mode, chatID)):
        
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


# --------------- START EXPENSE HANDLER --------------- #

@dp.callback_query_handler(text = ["expense"])
async def newExpense(call: types.CallbackQuery):


    if (usersManager.userExists(mode, call.message.chat.id)):
        await Expense.category.set()
        await call.message.answer("Introduce la categoría", reply_markup=getCategoriesKeyboard(call.message.chat.id))    
    else:
        await call.message.answer("No tienes acceso a este servicio")    


# CATEGORY SELECTION
@dp.message_handler(state=Expense.category)
async def process_name(message: types.Message, state: FSMContext):
    """
    Get Category
    Ask Price    
    """

    if (message.text[:-1] == 'Cancel'):
        await state.finish()

        await message.answer("❌ Cancelando...", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Selecciona una opción: ", reply_markup=ikMain)
    else:
        async with state.proxy() as data:

            data['category'] = message.text[:-1]

            key = getSubcategoriesKeyboard(message.chat.id, data['category'], True, "")

            if (not key):
                await Expense.next()        
                data['subcategory'] = None
                await Expense.next()        
                await message.answer("💰 Precio: ", reply_markup=ikNumeric)

            else:
                await Expense.next()
                await message.answer("Subcategoria: ", reply_markup=key)


# SUBCATEGORY SELECTION (optional)
@dp.message_handler(state=Expense.subcategory)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text[:-1] == 'Cancel'):
        await state.finish()

        await message.answer("❌ Cancelando...", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Selecciona una opción: ", reply_markup=ikMain)
    else:
        async with state.proxy() as data:
            # print(message.text[:-2])
            data['subcategory'] = message.text[:-1]

        await Expense.next()
        await message.answer("💰 Precio: ", reply_markup=ikNumeric)

# PRICE SELECTION
@dp.message_handler(state=Expense.price)
async def process_name(message: types.Message, state: FSMContext):
    """
    Get Price    
    Ask Date
    """
    userInput = message.text
    chatID = message.chat.id

    # Cancelar acción
    if (userInput[:-1] == 'Cancel'):
        await state.finish()
        await message.answer("❌ Cancelando...", reply_markup=ikMain)

    # Comprobamos que el formato del precio sea "5.95"
    elif (not isfloat(userInput) and not isfloat(userInput[:-1])):
        return await message.answer("❌ Formato incorrecto. Ejemplo: '5.58'", reply_markup=ikCancel)

    # Precio correcto
    else:    
        if (isfloat(userInput)):
            priceFormatted = userInput
        else:
            priceFormatted = userInput[:-1]
        

        await Expense.next()
        await state.update_data(price=priceFormatted)


        calendar, step = DetailedTelegramCalendar().build()
        
        await bot.send_message(chatID,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


# CALENDAR FUNCTION
@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=Expense.date)
async def inline_kb_answer_callback_handler(query, state: FSMContext):
    result, key, step = DetailedTelegramCalendar().process(query.data)

    chatID = query.message.chat.id
    messageID = query.message.message_id

    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    chatID,
                                    messageID,
                                    reply_markup=key)
    elif result:
        
        await bot.edit_message_text(f"You selected {result}",
                                    chatID,
                                    messageID)

        result = result.strftime('%d/%m/%Y')

        async with state.proxy() as proxy:
            proxy['date'] = result
        
        await Expense.next()
        await query.message.answer("🗒️ Descripcion: ", reply_markup=mkDescription)



# DESCRIPTION SELECTOR
@dp.message_handler(state=Expense.description)
async def get_price(message: types.Message, state: FSMContext):
    """
    Get Description
    Add Expense 
    """
    chatID = message.chat.id
    expenseDescription = message.text

    if (expenseDescription[:-1] == 'Cancel'):
        await state.finish()
        await message.answer("❌ Cancelando...", reply_markup=ikMain)
    else:
        
        if (expenseDescription == "Null"):
            desc  = "-"
        else:
            desc = message.text

        await Expense.next()
        await state.update_data(description=desc)

        async with state.proxy() as data:
            
            expenseObject = {
                'date': data['date'],
                'category': data['category'],
                'subcategory': data['subcategory'],
                'price': int(data['price']),
                'description': data['description']
            }

            # jsonManager.newExpense(chatID, data['date'], data['category'], data['subcategory'], data['price'], data['description'])
            # jsonManager.add_expense(mode, chatID, expenseObject)
            dbManager.newExpenseJson(mode, chatID, expenseObject)

            await message.answer('Nuevo gasto procesado correctamente ✅\n', reply_markup=types.ReplyKeyboardRemove())
            await bot.send_message(
                chatID,
                md.text(
                    md.text('Categoria:', md.code(data['category'])),
                    md.text('Subcategoría:', md.code(data['subcategory'])),
                    md.text('Precio:', data['price'], '€'),
                    md.text('Descripción:', data['description']),
                    md.text('Fecha:', data['date']),
                    sep='\n',
                ),
                reply_markup=ikMain,
                parse_mode=ParseMode.MARKDOWN,
            )

# ------------------ END EXPENSE HANDLER ---------------------- #












# ------- AUX FUNCS -----  #



def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def getCategoriesKeyboard(chatID):
    
    ikCategories = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    for elem in usersManager.getUserCategories(mode, chatID):
        ikCategories.insert(KeyboardButton(elem))

    ikCategories.add(KeyboardButton('Cancel❌'))

    return ikCategories

def getSubcategoriesKeyboard(chatID, parentCategoryID, markup, callback):
    # Creates Markup or Inline Keyboard. Callback Arg only for
    # Inline Keyboards

    with open(usersManager.getUserCategoriesFile(mode, chatID)) as f:
        data = json.load(f)

    if (markup):

        ikSubCategories = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        ikSubCategories.add(KeyboardButton('Cancel❌'))
        ikSubCategories.add(KeyboardButton('OtroX'))
        
        for elem in data:
            category = elem["category"]

            if (category.rstrip(category[-1]) == parentCategoryID
                and elem["subcategories"] != []):
                

                for subcat in elem["subcategories"]:
                    ikSubCategories.insert(KeyboardButton(subcat))            
        
                return ikSubCategories

    else:
        ikSubCategories = InlineKeyboardMarkup()

        for elem in data:
            category = elem["category"]

            if (category.rstrip(category[-1]) == parentCategoryID
                and elem["subcategories"] != []):
                
                ikSubCategories.insert(InlineKeyboardButton("TodasX", callback_data="/{}#{}".format(callback, "TodasX")))
                
                for subcat in elem["subcategories"]:
                    n = InlineKeyboardButton(text=subcat, callback_data="/{}#{}".format(callback, subcat))
                    ikSubCategories.insert(n)
                 
                ikSubCategories.insert(InlineKeyboardButton(text="Cancelar❌", callback_data="CancelX"))

        
                return ikSubCategories

    return False

db3 = KeyboardButton('Null')
mkDescription = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(db3, KeyboardButton('Cancel❌'))
pb10 = InlineKeyboardButton(text="Cancel", callback_data="cancel")
ikCancel = InlineKeyboardMarkup().add(pb10)
ikNumeric = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("1€", "2€", "5€", "10€", "20€", "50€", KeyboardButton('Cancel❌'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)