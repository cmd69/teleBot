# aiogram
from aiogram import types

# Local Imports
from telebot import dp, dbManager, keyboardFactory

#
# ----- Keyboards Setup ----- #
#

from handlers.main_handler import ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest, ikSettings

@dp.message_handler(commands=['newlink'])
async def welcome(message: types.Message):
    chatID = message.chat.id
    
    link = dbManager.create_link(chatID)
    if dbManager.user_exists(chatID):
        await message.answer("Tu link de acceso: " + link, reply_markup=ikMain)