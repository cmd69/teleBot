from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import aiogram.utils.markdown as md
from aiogram import types


# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory
from states import Expense
from utils import isfloat


# ----- Keyboards Setup ----- #
# ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain = keyboardFactory.get_default_keyboards()
from handlers.main_handler import ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest

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
                'price': float(data['price']),
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





