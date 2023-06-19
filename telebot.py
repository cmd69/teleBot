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
    port = app_config["PORT"]
    ip = app_config["IP"]
    subprocess.Popen(["streamlit", "run", app_path])
    subprocess.Popen(["streamlit", "run", app_path, "--server.port", port, "--server.address", ip])


if __name__ == "__main__":
    from handlers.main_handler import *
    from handlers.add_expense_handler import *
    from handlers.add_income_handler import *
    from handlers.fetch_month_handler import *
    from handlers.fetch_all_handler import *
    
    # Bot initialization
    bot_process = Process(target=run_bot)
    bot_process.start()
    
    # Streamlit initialization
    streamlit_process = Process(target=run_streamlit)
    streamlit_process.start()

    bot_process.join()
    streamlit_process.join()
    