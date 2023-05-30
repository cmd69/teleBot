from dotenv import load_dotenv

# Local Imports
from app import setup_flask, run_flask
from bot_setup import setup_bot
from aiogram import types

load_dotenv()

# Setup Flask
app = setup_flask()
# run_flask(app)

# Setup Bot
bot, dp, dbManager, usersManager, keyboardFactory, tablesFactory = setup_bot(app)




if __name__ == "__main__":
    from aiogram import executor
    from handlers import *
    # Import handlers after creating the Dispatcher
    
    
    executor.start_polling(dp, skip_updates=True)