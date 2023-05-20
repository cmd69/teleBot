import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()
DEBUG = False
PROD_DB_PATH = os.environ.get('PROD_DB_PATH')
PROD_BOT_TOKEN = os.environ.get('PROD_BOT_TOKEN')