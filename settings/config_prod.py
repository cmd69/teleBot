import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()
DEBUG = False
EXPENSES_DB_PATH = os.environ.get('PROD_DB_PATH')
USERS_DB_PATH = os.environ.get('PROD_USERS_DB_PATH')
BOT_TOKEN = os.environ.get('PROD_BOT_TOKEN')
MODE = os.environ.get('PROD_MODE')
IP = os.environ.get('PROD_IP')
PORT = os.environ.get('PROD_PORT')