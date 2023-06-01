# aiogram
from aiogram.types import ParseMode
from aiogram import types


# Local Imports
from telebot import dp, bot, dbManager, keyboardFactory, tablesFactory




# ----- Keyboards Setup ----- #
# ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain = keyboardFactory.get_default_keyboards()
from handlers.main_handler import ikPortfolio, ikFetchData, ikBenz, mkDescription, ikCancel, ikNumeric, ikMain, ikGuest

@dp.callback_query_handler(text = ["general"])
async def newExpense(call: types.CallbackQuery):

    chatID = call.message.chat.id
    messageID = call.message.message_id
    if (dbManager.user_exists(chatID)):

        report = tablesFactory.generate_general_report(dbManager.get_all_expenses(chatID))
        await bot.edit_message_text(f'<pre>GASTOS GENERALES</pre> <pre>{report}</pre>',
                                        chatID,
                                        messageID,
                                        parse_mode=ParseMode.HTML)
        await bot.edit_message_reply_markup(chatID,
                                            messageID,
                                            reply_markup=ikMain)
    else:
        await call.message.answer("No tienes acceso a este servicio")   