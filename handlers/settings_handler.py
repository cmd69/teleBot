# aiogram
from aiogram import types

# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory


# Aux imports
import os

#
# ----- Keyboards Setup ----- #
#
from handlers.main_handler import ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest, ikSettings


# Main Menu
@dp.callback_query_handler(text = ["settings"])
async def random_value(call: types.CallbackQuery):
    
    chatID = call.message.chat.id
    messageID = call.message.message_id

    await bot.edit_message_text("Mostrando menu de opciones... ",
                                    chatID,
                                    messageID)
            
    await bot.edit_message_reply_markup(
                                    chatID,
                                    messageID,
                                    inline_message_id= None,
                                    reply_markup=ikSettings)





@dp.callback_query_handler(text = ["exit_demo"])
async def newExpense(call: types.CallbackQuery):
    chatID = call.message.chat.id
    messageID = call.message.message_id

    dbManager.exit_demo_mode(chatID)

    await bot.edit_message_text("Saliendo del modo demo... ",
                                    chatID,
                                    messageID)
            
    await bot.edit_message_reply_markup(
                                    chatID,
                                    messageID,
                                    inline_message_id= None,
                                    reply_markup=ikPortfolio)
