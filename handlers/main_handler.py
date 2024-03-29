# aiogram
from aiogram import types

# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory

# Aux imports
import os

#
# ----- Keyboards Setup ----- #
#

ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest, ikSettings = keyboardFactory.get_default_keyboards()

# /Start and /Help
@dp.message_handler(commands=['test'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    messageID = message.message_id
    # c = dbManager.migrateSheetsToJson("dev", chatID, '22/05/2022', '22/05/2023')
    # c = dbManager.get_expenses_from_sheets('22/05/2022')
    expense = {
        "date": "30/05/2023",
        "category": "Comida",
        "subcategory": "Snacks",
        "price": 10,
        "description": "Merienda"
    }
    income = {
        "date": "30/05/2023",
        "price": 100000,
        "description": "Nómina"
    }
    consult = {
        'date': "30/05/2023",
        'category': "Todas",
        'subcategory': None
    }
    
    pass

# /Start and /Help
@dp.message_handler(commands=['loadSheets'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    if dbManager.load_expenses_from_sheets_to_json(chatID):
        await message.answer("Gastos cargados de Sheets Correctamente!", reply_markup=ikMain)
    else:
        await message.answer("Parece que ha habido un error...", reply_markup=ikMain)

    

# /Start and /Help
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    
    chatID = message.chat.id
    messageID = message.message_id
    if (dbManager.user_exists(chatID)):
        await message.answer("Hola, bienvenido a tu gestor de portfolio!", reply_markup=ikMain)
    else:
        await message.answer("Hola, bienvenido a tu gestor de portfolio! Parece que eres nuevo" +
            " pero no te preocupes, porque puedes comenzar a usar la app sin registrarte!\n\n" +
            " Si le das a probar demo, se cargarán datos de prueba, y comenzando desde 0 podrás" +
            " empezar a guardar tus gastos.", reply_markup=ikGuest)


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



















