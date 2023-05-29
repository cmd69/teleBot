import os
from dotenv import load_dotenv
from flask import Flask
import threading
import datetime


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types




# Local Imports
from keyboardsGenerator import KeyboardsGenerator
from tablesGenerator import TableGenerator
from DBManager import DBManager

## Import the button dictionaries from separate files
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from database.keyboards.portfolio_keyboard import portfolio_buttons
from database.keyboards.fetch_data_keyboard import fetch_data_buttons
from database.keyboards.benz_keyboard import benz_buttons
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot_calendar import DetailedTelegramCalendar, MonthTelegramCalendar, LSTEP
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


dbManager = DBManager(mode)
usersManager = dbManager.get_users_manager()
keyboardFactory = KeyboardsGenerator(usersManager)
tablesFactory = TableGenerator(usersManager)



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
@dp.message_handler(commands=['updateJson'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    messageID = message.message_id
    # c = dbManager.migrateSheetsToJson("dev", chatID, '22/05/2022', '22/05/2023')
    # c = dbManager.get_expenses_from_sheets('22/05/2022')
    expense = {
        "date": "30/05/2023",
        "category": "Comida",
        "subcategory": "Snacks",
        "price": 100000,
        "description": "SnickersChuches"
    }
    income = {
        "date": "30/05/2023",
        "price": 100000,
        "description": "SnickersChuches"
    }
    
    # c = dbManager.get_expenses_from_sheets("01/05/2023")
    dbManager.add_expense(chatID, expense)
    dbManager.add_income(chatID, income)
    dbManager.delete_income(chatID, income)
    dbManager.delete_expense(chatID, expense)
    

# /Start and /Help
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    
    chatID = message.chat.id
    messageID = message.message_id
    
    await message.answer("Hola, bienvenido a tu gestor de portfolio!", reply_markup=ikMain)
    # sheetsManager.getMonthIncomes(mode, chatID, "22/05/2023")



# Main Menu
@dp.callback_query_handler(text = ["portfolio", "benz"])
async def random_value(call: types.CallbackQuery):
    
    chatID = call.message.chat.id
    messageID = call.message.message_id

    if (dbManager.user_exists(chatID)):
        
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


# Back Button
@dp.callback_query_handler(text = ["back"])
async def backButton(call: types.CallbackQuery):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    
    await bot.edit_message_text("Volviendo atrás...", chatID, messageID)
            
    await bot.edit_message_reply_markup( chatID, messageID,
                            inline_message_id= None,
                            reply_markup=ikMain)


# --------------- START EXPENSE HANDLER --------------- #

@dp.callback_query_handler(text = ["expense"])
async def newExpense(call: types.CallbackQuery):


    if (dbManager.user_exists(call.message.chat.id)):
        await Expense.category.set()
        await call.message.answer("Introduce la categoría", reply_markup=keyboardFactory.getCategoriesKeyboard(call.message.chat.id))    
    else:
        await call.message.answer("No tienes acceso a este servicio")    


# CATEGORY SELECTION
@dp.message_handler(state=Expense.category)
async def process_name(message: types.Message, state: FSMContext):
    """
    Get Category
    Ask Price    
    """
    chatID = message.chat.id
    if (message.text[:-1] == 'Cancel'):
        await state.finish()

        await message.answer("❌ Cancelando...", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Selecciona una opción: ", reply_markup=ikMain)
    else:
        async with state.proxy() as data:

            data['category'] = message.text[:-1]


            key = keyboardFactory.getSubcategoriesKeyboard(chatID, data['category'], True, "")

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

            # dbManager.newExpenseJson(mode, chatID, expenseObject)
            # c = dbManager.newExpense(mode, chatID, expenseObject)
            dbManager.add_expense(chatID, expenseObject)


            await message.answer('Nuevo ingreso procesado correctamente ✅\n', reply_markup=types.ReplyKeyboardRemove())
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


# Cancel Button (Not in use)
@dp.callback_query_handler(text = ["cancel"], state=Expense)
async def cancelButton(call: types.CallbackQuery, state: FSMContext):
    await state.finish()    
    
    chatID = call.message.chat.id
    messageID = call.message.message_id
    
    # await call.message.answer("❌ Cancelando...", reply_markup=ikMain)

    await bot.edit_message_text("❌ Cancelando...",
                                    chatID,
                                    messageID)

    await bot.edit_message_reply_markup(
                                chatID,
                                messageID,
                                inline_message_id= None,
                                reply_markup=ikMain)  

# ------------------ END EXPENSE HANDLER ---------------------- #




@dp.callback_query_handler(text = ["general"])
async def newExpense(call: types.CallbackQuery):

    chatID = call.message.chat.id
    messageID = call.message.message_id
    if (dbManager.user_exists(chatID)):

        report = tablesFactory.generate_general_report(dbManager.get_all_expenses(chatID))
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
    if (dbManager.user_exists(chatID)):
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

            dbManager.add_income(chatID, income)

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

    if (dbManager.user_exists(chatID)):

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

    
    categories = usersManager.get_user_categories(chatID)
    paginator = keyboardFactory.paginatorFactory(categories, 1, 9, "filter", "categorySelection", False)        
        

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
    categories =  usersManager.get_user_categories(chatID)
    page = int(call.data.split('#')[1])  
    paginator = keyboardFactory.paginatorFactory(categories, page, 9, "filter", "categorySelection", False)

    
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
        
        consult = {
            'date': str(fetchMonth),
            'category': "Todas",
            'subcategory': None
        }

        table = tablesFactory.generate_month_recap(consult, dbManager.get_expenses(chatID, consult))
        
        await bot.edit_message_text(f'<pre>GASTOS DE {monthStr.upper()}</pre> <pre>{table}</pre>',
                                        chatID,
                                        messageID,
                                        parse_mode=ParseMode.HTML)

        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=ikMain)

    else:
     
        
        key = keyboardFactory.getSubcategoriesKeyboard(chatID, category, False, "subcategorySelection")
        
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

                       
            consult = {
                'date': str(fetchMonth),
                'category': category,
                'subcategory': None
            }

            expenses = dbManager.get_expenses(chatID, consult)
            table = tablesFactory.generate_month_recap(consult, expenses)

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
    subcategory = subcategory.rstrip(subcategory[-1])
    month = datetime.date.today().strftime('%d/%m/%Y')


    async with state.proxy() as data:
        data['subcategory'] = subcategory
        fetchMonth = data['date']
        cat = data['category']

        await state.finish()

        monthStr = datetime.datetime.strptime(fetchMonth, "%d/%m/%Y")
        monthStr = datetime.datetime.strftime(monthStr, "%B-%y")
        

        consult = {
            'date': fetchMonth,
            'category': cat,
            'subcategory': subcategory
        }


        table = tablesFactory.generate_month_recap(consult, dbManager.get_expenses(chatID, consult))


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

            categories = usersManager.get_user_categories(chatID)
            paginator = keyboardFactory.paginatorFactory(categories, 1, 9, "filter", "categorySelection", False)        
                

            # TODO Mostrar Stats Generales
            await bot.edit_message_text("Deseas seleccionar algun filtro?",
                                        chatID,
                                        messageID)

            await bot.edit_message_reply_markup(chatID, messageID,
                                        inline_message_id= None,
                                        reply_markup=paginator.markup)


# Cancel Button (Not in use)
@dp.callback_query_handler(text = ["cancel"], state=FetchFilters)
async def cancelButton(call: types.CallbackQuery, state: FSMContext):
    await state.finish()    
    
    chatID = call.message.chat.id
    messageID = call.message.message_id
    
    # await call.message.answer("❌ Cancelando...", reply_markup=ikMain)

    await bot.edit_message_text("❌ Cancelando...",
                                    chatID,
                                    messageID)

    await bot.edit_message_reply_markup(
                                chatID,
                                messageID,
                                inline_message_id= None,
                                reply_markup=ikMain) 


# --------------- END FETCH --------------- #






# ------- AUX FUNCS -----  #




def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False



db3 = KeyboardButton('Null')
mkDescription = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(db3, KeyboardButton('Cancel❌'))
pb10 = InlineKeyboardButton(text="Cancel", callback_data="cancel")
ikCancel = InlineKeyboardMarkup().add(pb10)
ikNumeric = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("1€", "2€", "5€", "10€", "20€", "50€", KeyboardButton('Cancel❌'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)