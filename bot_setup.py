from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from managers.db_manager import DBManager
from generators.keyboards_generator import KeyboardsGenerator
from generators.tables_generator import TableGenerator

def setup_bot(app):
    bot = Bot(token=app.config["BOT_TOKEN"])
    storage = MemoryStorage()  # external storage is supported!
    dp = Dispatcher(bot, storage=storage)

    dbManager = DBManager(app.config["MODE"])
    usersManager = dbManager.get_users_manager()
    keyboardFactory = KeyboardsGenerator(usersManager)
    tablesFactory = TableGenerator(usersManager)

    return bot, dp, dbManager, usersManager, keyboardFactory, tablesFactory
