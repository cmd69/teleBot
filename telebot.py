from aiogram import executor

# Local Imports
from app import setup_flask
from bot_setup import setup_bot



# Setup Flask
app = setup_flask()

# Setup Bot
bot, dp, dbManager, keyboardFactory, tablesFactory = setup_bot(app)


if __name__ == "__main__":
    
    
    # Import handlers after creating the Dispatcher
    from handlers.main_handler import *
    from handlers.add_expense_handler import *
    from handlers.add_income_handler import *
    from handlers.fetch_month_handler import *
    from handlers.fetch_all_handler import *
    
    executor.start_polling(dp, skip_updates=True)