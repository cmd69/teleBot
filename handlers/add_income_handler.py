from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import aiogram.utils.markdown as md
from aiogram import types


# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory
from states import Income
from utils import isfloat


# ----- Keyboards Setup ----- #
ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain = keyboardFactory.get_default_keyboards()




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
