# aiogram
from aiogram import types

# Local Imports
from telebot import dp, dbManager, keyboardFactory

ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest = keyboardFactory.get_default_keyboards()


@dp.message_handler(commands=['link'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    await message.answer("Enviando link de acceso")
    
    link = dbManager.get_link(chatID)
    if dbManager.user_exists(chatID):
        await message.answer("Tu link de acceso: " + link, reply_markup=ikMain)

