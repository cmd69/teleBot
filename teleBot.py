import os
from dotenv import load_dotenv
from flask import Flask
import dbManager
import jsonManager
import usersManager
import json
import threading
import asyncio
import sheetsManager
import datetime
import calendar


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

from telegram_bot_calendar import DetailedTelegramCalendar, MonthTelegramCalendar, LSTEP
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from datetime import date, timedelta, datetime
import dateutil.relativedelta


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

portfolio_buttons = {
    "income": "Ingreso",
    "expense": "Gasto",
    "fetch": "Consultar",
    "deleteExpense": "Eliminar Gasto",
    "back": "Atras ↩️"
}

fetch_data_buttons = {
    "general": "General",
    "currMonth": "Este Mes",
    "lastMonth": "Mes Pasado",
    "customMonth": "Otro Mes",
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

class Income(StatesGroup):
    date = State()
    price = State()
    description = State()

class FetchFilters(StatesGroup):
    date = State()
    filter = State()
    category = State()
    subcategory = State()

class Fill(StatesGroup):
    price = State()
    diesel = State()
    date = State()




# /Start and /Help
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    messageID = message.message_id
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


        calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
        
        await bot.send_message(chatID,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


# CALENDAR FUNCTION
@dp.callback_query_handler(DetailedTelegramCalendar.func(calendar_id=1), state=Expense.date)
async def inline_kb_answer_callback_handler(query, state: FSMContext):
    result, key, step = DetailedTelegramCalendar(calendar_id=1).process(query.data)

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




@dp.callback_query_handler(text = ["general"])
async def newExpense(call: types.CallbackQuery):

    chatID = call.message.chat.id
    messageID = call.message.message_id
    if (usersManager.userExists(mode, chatID)):

        report = generate_overall_report(jsonManager.getExpenses("dev", chatID))
        # await call.message.edit_reply_markup(f'{report}', reply_markup=ikPortfolio)
        # await call.message.edit_reply_markup(f'{report}', reply_markup=ikPortfolio)
        
        await bot.edit_message_text(f'<pre>GASTOS GENERALES</pre> <pre>{report}</pre>',
                                        chatID,
                                        messageID,
                                        parse_mode=ParseMode.HTML)

        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=ikMain)
    else:
        await call.message.answer("No tienes acceso a este servicio")   














# --------------- START INCOMMMMMMEEEE HANDLER --------------- #

@dp.callback_query_handler(text = ["income"])
async def newExpense(call: types.CallbackQuery):

    chatID = call.message.chat.id
    messageID = call.message.message_id
    if (usersManager.userExists(mode, chatID)):
        await Income.date.set()
        calendar, step = DetailedTelegramCalendar(calendar_id=3).build()
        

        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                chatID,
                                messageID)

        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=calendar)

    else:
        await call.message.answer("No tienes acceso a este servicio")    


# CALENDAR FUNCTION
@dp.callback_query_handler(DetailedTelegramCalendar.func(calendar_id=3), state=Income.date)
async def inline_kb_answer_callback_handler(query, state: FSMContext):
    """
    Get Date
    Ask Price    
    """
    
    result, key, step = DetailedTelegramCalendar(calendar_id=3).process(query.data)

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
        
        await Income.next()
        await query.message.answer("💰 Precio: ", reply_markup=ikNumeric)



# PRICE SELECTION
@dp.message_handler(state=Income.price)
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
        

        await Income.next()
        await state.update_data(price=priceFormatted)


        
        await message.answer("🗒️ Descripcion: ", reply_markup=mkDescription)

# DESCRIPTION SELECTOR
@dp.message_handler(state=Income.description)
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
        
        if (expenseDescription == "Null" or expenseDescription == " "):
            desc  = "-"
        else:
            desc = message.text

        await Income.next()
        await state.update_data(description=desc)

        async with state.proxy() as data:
            
            income = {
                'date': data['date'],
                'price': round(float(data['price']),2),
                'description': data['description']
            }

            dbManager.newIncomeJson(mode, chatID, income)

            await message.answer('Nuevo gasto procesado correctamente ✅\n', reply_markup=types.ReplyKeyboardRemove())
            await bot.send_message(
                chatID,
                md.text(
                    md.text('Fecha:', data['date']),
                    md.text('Precio:', data['price'], '€'),
                    md.text('Descripción:', data['description']),                   
                    sep='\n',
                ),
                reply_markup=ikMain,
                parse_mode=ParseMode.MARKDOWN,
            )

# --------------- ENDDDDD INCOMMMMMMEEEE HANDLER --------------- #












# --------------- START FETCH --------------- #

# Fetch Button
@dp.callback_query_handler(text = ["fetch"])
async def fetchExpenses(call: types.CallbackQuery):

    chatID = call.message.chat.id
    messageID = call.message.message_id

    if (usersManager.userExists(mode, chatID)):

        await bot.edit_message_text("Selecciona el consumo que quieres ver... ",
                                    chatID,
                                    messageID)

        await bot.edit_message_reply_markup(
                                    chatID,
                                    messageID,
                                    inline_message_id= None,
                                    reply_markup=ikFetchData)
        
    else:
        await call.message.answer("No tienes acceso a este servicio")  


# Handler para acceso rapido a mes actual y pasado. Creación de teclado de filtros.
@dp.callback_query_handler(text = ["currMonth", "lastMonth"])
async def fetchAll(call: types.CallbackQuery, state: FSMContext):

    
    chatID = call.message.chat.id
    messageID = call.message.message_id
    
    month = call.data
    currDate = datetime.date.today().strftime('%d/%m/%Y')
    
    await FetchFilters.date.set()

    async with state.proxy() as data:
        if (month == "currMonth"):
            data['date'] = currDate
        else:
            lastMonth = datetime.datetime.strptime(currDate, '%d/%m/%Y') - dateutil.relativedelta.relativedelta(months=1)
            lastMonth = datetime.datetime.strftime(lastMonth, '%d/%m/%Y')
            data['date'] = lastMonth
        
    await FetchFilters.next()    

    
    categories = usersManager.getUserCategories(mode, chatID)
    paginator = paginatorFactory(categories, 1, 9, "filter", "categorySelection", False)        
        

    # TODO Mostrar Stats Generales
    await bot.edit_message_text("Deseas seleccionar algun filtro?",
                                chatID,
                                messageID)

    await bot.edit_message_reply_markup(
                                chatID,
                                messageID,
                                inline_message_id= None,
                                reply_markup = paginator.markup)



# Handler para cambiar de pagina
# state=FetchFilters.filter
@dp.callback_query_handler(lambda text: str(text.data).split('#')[0] == '/filter', state=FetchFilters.filter)
async def inline_kb_answer_callback_handler(call: types.CallbackQuery, state: FSMContext):

    chatID = call.message.chat.id
    messageID = call.message.message_id
    categories =  usersManager.getUserCategories(mode, chatID)
    page = int(call.data.split('#')[1])  
    paginator = paginatorFactory(categories, page, 9, "filter", "categorySelection", False)

    
    await bot.edit_message_text("Deseas seleccionar algun filtro?",
        chatID,
        messageID,
        parse_mode='Markdown'
    )

    await bot.edit_message_reply_markup(
        chatID,
        messageID,
        reply_markup=paginator.markup
    )


@dp.callback_query_handler(lambda text: str(text.data).split('#')[0] == '/categorySelection', state=FetchFilters.filter)
async def inline_kb_answer_callback_handler(call: types.CallbackQuery, state: FSMContext):
    
    

    chatID = call.message.chat.id
    messageID = call.message.message_id

    category = str(call.data).split('#')[1]
    category = category.rstrip(category[-1])

    if (category == "Todas"):

        async with state.proxy() as data:
            data['filter'] = False
            data['category'] = category
            data['subcategory'] = False
            fetchMonth = data['date']
            
        await state.finish()

        try:
            monthStr = datetime.datetime.strptime(str(fetchMonth), "%d/%m/%Y")
            monthStr = datetime.datetime.strftime(monthStr, "%B-%y")
        except:
            monthStr = datetime.datetime.strftime(fetchMonth, "%B-%y")    
        

        table = createExpensesTable(chatID, fetchMonth, False, category, False)
        
        await bot.edit_message_text(f'<pre>GASTOS DE {monthStr.upper()}</pre> <pre>{table}</pre>',
                                        chatID,
                                        messageID,
                                        parse_mode=ParseMode.HTML)

        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=ikMain)

    else:
     
        
        key = getSubcategoriesKeyboard(chatID, category, False, "subcategorySelection")
        
        if ( key != False):

            async with state.proxy() as data:
                data['filter'] = True
                await FetchFilters.next()
                data['category'] = category
                await FetchFilters.next()

            

            await bot.edit_message_text("Selecciona la subcategoria de " + str(call.data).split('#')[1],
                                        chatID,
                                        messageID)

            await bot.edit_message_reply_markup(
                                        chatID,
                                        messageID,
                                        inline_message_id= None,
                                        reply_markup=key) 
        else:

            async with state.proxy() as data:
                data['filter'] = True
                await FetchFilters.next()
                data['category'] = category
                await FetchFilters.next()
                data["subcategory"] = False
                fetchMonth = data['date']
            
            await state.finish()
            
            monthStr = datetime.datetime.strptime(fetchMonth, "%d/%m/%Y")
            monthStr = datetime.datetime.strftime(monthStr, "%B-%y")

            table = createExpensesTable(chatID, fetchMonth, True, category, False)

            await bot.edit_message_text(f'<pre>GASTOS DE {monthStr.upper()}</pre> <pre>{table}</pre>',
                                            chatID,
                                            messageID,
                                            parse_mode=ParseMode.HTML)

            await bot.edit_message_reply_markup(chatID,
                                                messageID,
                                                reply_markup=ikMain)

# , state=FetchFilters.subcategory
@dp.callback_query_handler(lambda text: str(text.data).split('#')[0] == '/subcategorySelection', state=FetchFilters.subcategory)
async def inline_kb_answer_callback_handler(call: types.CallbackQuery, state: FSMContext):


    chatID = call.message.chat.id
    messageID = call.message.message_id
    
    subcategory = str(call.data).split('#')[1]
    month = datetime.date.today().strftime('%d/%m/%Y')


    async with state.proxy() as data:
        data['subcategory'] = subcategory
        fetchMonth = data['date']
        cat = data['category']

        await state.finish()

        monthStr = datetime.datetime.strptime(fetchMonth, "%d/%m/%Y")
        monthStr = datetime.datetime.strftime(monthStr, "%B-%y")
        

        table = createExpensesTable(chatID, fetchMonth, True, cat, subcategory)

        await bot.edit_message_text(f'<pre>GASTOS DE {monthStr.upper()}</pre> <pre>{table}</pre>',
                                        chatID,
                                        messageID,
                                        parse_mode=ParseMode.HTML)

        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=ikMain)



@dp.callback_query_handler(text = ["customMonth"])
async def fetchCustomMonth(call: types.CallbackQuery):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    await FetchFilters.date.set()
    
    calendar, step = MonthTelegramCalendar(calendar_id=2).build()

    
        
    await bot.edit_message_text(f"Select {LSTEP[step]}",
                                chatID,
                                messageID)

    await bot.edit_message_reply_markup(chatID,
                                        messageID,
                                        reply_markup=calendar)
                                        

@dp.callback_query_handler(MonthTelegramCalendar.func(calendar_id=2), state=FetchFilters.date)
async def inline_kb_answer_callback_handler(call, state: FSMContext):
    
    chatID = call.message.chat.id
    messageID = call.message.message_id
    result, key, step = MonthTelegramCalendar(calendar_id=2).process(call.data)
    
    
    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    chatID,
                                    messageID,
                                    reply_markup=key)
    elif result:
        
        result = result.strftime('%d/%m/%Y')

        async with state.proxy() as proxy:
            proxy['date'] = result
            await FetchFilters.next()

            categories = usersManager.getUserCategories(mode, chatID)
            paginator = paginatorFactory(categories, 1, 9, "filter", "categorySelection", False)        
                

            # TODO Mostrar Stats Generales
            await bot.edit_message_text("Deseas seleccionar algun filtro?",
                                        chatID,
                                        messageID)

            await bot.edit_message_reply_markup(chatID, messageID,
                                        inline_message_id= None,
                                        reply_markup=paginator.markup)


# --------------- END FETCH --------------- #









# ------- AUX FUNCS -----  #


# Plantilla para la creación de los gastos mensuales (Dia, Categoria, Descripcion)
def createExpensesTable(chatID, date, filter, category, subcategory):


    table = pt.PrettyTable(['📅', '🔰', '💸'])
    table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]


    try:
        subcategory = subcategory.rstrip(subcategory[-1])
    except:
        pass

    fetchObject = {
        'date': date,
        'category': category,
        'subcategory': subcategory
    }
    
    expenses, tIncome, tExpenses = dbManager.getMonthExpensesJson(mode, chatID, fetchObject)
    total_expenses = 0

    # 1 Mostrar TODOS los gastos
    # 2 Mostrar subcategorias de una categoria
    if (not filter or not subcategory):
        table.field_names = ["Date 📅", "Cat. 🔰", "Price 💸"]
        # Add rows to the table and calculate total expenses
        for expense in expenses:
            day = expense['date'].split('/')[0]
            category = expense['category']
            price = expense['price']
            table.add_row([day, category, f"${price}"])
            total_expenses += round(float(price), 2)
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
    remaining = tIncome - total_expenses
    # table.bottom_junction_char("-")
    # Add a row for total expenses, income, and remaining
    # table.add_row(['T', '-', str(1000) + ' €'])
    table.add_row(['Expenses', '-', f"{round(total_expenses,2)} €"])
    table.add_row(['Income', '-', f"{round(tIncome,2 )} €"])
    table.add_row(['Saved', '-', f"{round(remaining, 2)} €"])

    
    

    # Decorate the table with emojis
    # table.set_style(9)  # Choose a fancy table style
    table.align = "l"
    table.padding_width = 1
    table.format = True

    # Create a string with the formatted table
    formatted_table = f"Income: {round(tIncome,2)} € \nExpenses: {round(total_expenses,2)} €\nSaved: {round(remaining,2)} € \n\n{table}"

    return formatted_table

def generate_overall_report2(json_data):
    recap_message = "💰 Budget Recap 💰\n\n"
    
    years = json_data["years"]
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
        recap_message += f"💵 Avg. Income:\t €{average_income:.0f}\n"
    
    # Calculate average expenses
    if total_expenses_count > 0:
        average_expenses = total_expenses / total_expenses_count
        recap_message += f"💸 Avg. Expenses:\t €{average_expenses:.0f} ({(average_expenses / total_income) * 100:.0f}%)\n"
    
    # Calculate average saved
    average_saved = average_income - average_expenses
    recap_message += f"💰 Avg. Saved:\t €{average_saved:.0f} ({(average_saved / total_income) * 100:.0f}%)\n\n"
    
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
    
    recap_message += "📊 Category Averages\n\n"
    
    for category, data in categories.items():
        average_expense = data["total"] / data["count"]
        percentage_of_expenses = (data["total"] / total_expenses) * 100
        recap_message += f"{category}:\t €{average_expense:.0f}\t ({percentage_of_expenses:.0f}%)\n"
    
    return recap_message

def generate_overall_report(json_data):
    recap_message = "💰 Budget Recap 💰\n\n"
    
    years = json_data["years"]
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







# Create any paginator
def paginatorFactory(elements, page, gridSize, footerCommand, callbackCommand, expenses):
    
    
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