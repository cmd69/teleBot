from aiogram import executor
# Local Imports
from bot_setup import setup_bot, setup_config
from multiprocessing import Process
import subprocess


# Setup Flask
app_config = setup_config()

# Setup Bot
bot, dp, dbManager, keyboardFactory, tablesFactory, chartsGenerator = setup_bot(app_config)


def run_bot():

    
    executor.start_polling(dp, skip_updates=True)


def run_streamlit():
    app_path = "streamlit_app.py"
    subprocess.Popen(["streamlit", "run", app_path])


if __name__ == "__main__":
    from handlers.main_handler import *
    from handlers.add_expense_handler import *
    from handlers.add_income_handler import *
    from handlers.fetch_month_handler import *
    from handlers.fetch_all_handler import *
    bot_process = Process(target=run_bot)
    streamlit_process = Process(target=run_streamlit)

    bot_process.start()
    streamlit_process.start()

    bot_process.join()
    streamlit_process.join()
    
    # Import handlers after creating the Dispatcher
    