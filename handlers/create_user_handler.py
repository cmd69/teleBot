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


# New user
@dp.callback_query_handler(text = ["new_user", "new_demo"])
async def random_value(call: types.CallbackQuery):
    chatID = call.message.chat.id
    messageID = call.message.message_id

    # if call.data == "new_guest":
    await bot.send_message(chatID, "Please enter your username:")
    
    # Register a new message handler to capture the username
    @dp.message_handler(chat_id=chatID)
    async def get_username(message: types.Message):
        username = message.text
        dbManager.create_new_user(chatID, username)
        await message.answer("Perfecto, ya está todo listo!\nPuedes empezar añadiendo gastos seleccionando `portfolio`",
                        reply_markup=ikPortfolio)
    