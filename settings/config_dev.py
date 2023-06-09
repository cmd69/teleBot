import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()
DEBUG = True
DB_PATH = os.environ.get('DEV_DB_PATH')
USERS_DB_PATH = os.environ.get('DEV_USERS_DB_PATH')
BOT_TOKEN = os.environ.get('DEV_BOT_TOKEN')
MODE = os.environ.get('DEV_MODE')
IP = os.environ.get('DEV_IP')
PORT = os.environ.get('DEV_PORT')