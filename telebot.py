# Local Imports
from app import setup_flask
from bot_setup import setup_bot
from aiogram import types

# Libraries
from dotenv import load_dotenv



load_dotenv()

# Setup Flask
app = setup_flask()

# Setup Bot
bot, dp, dbManager, usersManager, keyboardFactory, tablesFactory = setup_bot(app)


if __name__ == "__main__":
    from aiogram import executor
    # Import handlers after creating the Dispatcher
    from handlers import *
    
    
    
    executor.start_polling(dp, skip_updates=True)