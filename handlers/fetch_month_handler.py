from telegram_bot_calendar import MonthTelegramCalendar, LSTEP

# aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram import types


# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory, tablesFactory
from states import FetchFilters


# others
import dateutil.relativedelta
import datetime


# ----- Keyboards Setup ----- #
# ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain = keyboardFactory.get_default_keyboards()
from handlers.main_handler import ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest

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

    
    
    paginator = keyboardFactory.paginatorFactory(chatID, 1, 9, "filter", "categorySelection", False)        
        

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
    page = int(call.data.split('#')[1])  
    paginator = keyboardFactory.paginatorFactory(chatID, page, 9, "filter", "categorySelection", False)

    
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
        expenses = dbManager.get_expenses(chatID, consult)
        incomes = dbManager.get_incomes(chatID, consult)
        table = tablesFactory.generate_month_recap(consult, expenses, incomes)
        
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
            incomes = dbManager.get_incomes(chatID, consult)
            table = tablesFactory.generate_month_recap(consult, expenses, incomes)

            await bot.edit_message_text(f'<pre>GASTOS DE {monthStr.upper()}</pre> <pre>{table}</pre>',
                                            chatID,
                                            messageID,
                                            parse_mode=ParseMode.HTML)

            await bot.edit_message_reply_markup(chatID,
                                                messageID,
                                                reply_markup=ikMain)


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

        expenses = dbManager.get_expenses(chatID, consult)
        incomes = dbManager.get_incomes(chatID, consult)
        table = tablesFactory.generate_month_recap(consult, expenses, incomes)


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

            paginator = keyboardFactory.paginatorFactory(chatID, 1, 9, "filter", "categorySelection", False, )

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

    await bot.edit_message_text("❌ Cancelando...",
                                    chatID,
                                    messageID)

    await bot.edit_message_reply_markup(
                                chatID,
                                messageID,
                                inline_message_id= None,
                                reply_markup=ikMain) 


# --------------- END FETCH --------------- #