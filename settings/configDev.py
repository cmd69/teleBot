import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

DEV_DB_PATH = os.environ.get('DEV_DB_PATH')
DEV_BOT_TOKEN = os.environ.get('DEV_BOT_TOKEN')