# Local Imports
from managers.users_manager import UsersManager
from managers.db_manager import DBManager
from generators.tables_generator import TableGenerator
from generators.keyboards_generator import KeyboardsGenerator
from generators.charts_generator import ChartsGenerator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Libraries
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

def setup_config():
    mode = os.environ.get('TELEBOT_ENV', 'dev')  # Default to development mode if not specified

    if mode == 'prod':
        config_file = os.environ.get('PROD_SETTINGS_FILE')
    else:
        config_file = os.environ.get('DEV_SETTINGS_FILE')

    # Load the configuration from the file
    config = {}
    
    
    with open(config_file) as f:
        exec(f.read(), config)

    return config


def setup_bot(app_config):
    bot = Bot(token=app_config["BOT_TOKEN"])
    storage = MemoryStorage()  # external storage is supported!
    dp = Dispatcher(bot, storage=storage)

    usersManager = UsersManager(app_config["USERS_DB_PATH"], app_config["PORT"], app_config["IP"])
    dbManager = DBManager(usersManager, app_config["MODE"])
    keyboardFactory = KeyboardsGenerator(usersManager)
    tablesFactory = TableGenerator(usersManager)
    chartsGenerator = ChartsGenerator(dbManager)

    return bot, dp, dbManager, keyboardFactory, tablesFactory, chartsGenerator
