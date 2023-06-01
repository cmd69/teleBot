# Local Imports
from managers.users_manager import UsersManager
from managers.db_manager import DBManager
from generators.tables_generator import TableGenerator
from generators.keyboards_generator import KeyboardsGenerator


# Libraries
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage



def setup_bot(app):
    bot = Bot(token=app.config["BOT_TOKEN"])
    storage = MemoryStorage()  # external storage is supported!
    dp = Dispatcher(bot, storage=storage)

    usersManager = UsersManager(app.config["USERS_DB_PATH"])
    dbManager = DBManager(usersManager, app.config["MODE"])
    keyboardFactory = KeyboardsGenerator(usersManager)
    tablesFactory = TableGenerator(usersManager)

    return bot, dp, dbManager, keyboardFactory, tablesFactory
