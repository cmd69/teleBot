import os
import threading
from flask import Flask
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

def setup_flask():
    app = Flask(__name__)
    mode = os.environ.get('TELEBOT_ENV', 'dev')  # Default to development mode if not specified
    c = os.environ.get('PROD_SETTINGS_FILE')
    print(c)

    if mode == 'prod':
        app.config.from_pyfile(os.environ.get('PROD_SETTINGS_FILE'))
    else:
        app.config.from_pyfile(os.environ.get('DEV_SETTINGS_FILE'))

    return app


def run_flask(app):
    if app.config.get('DEBUG', False):
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': 8080, 'host': '192.168.1.148'})
    else:
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False, 'port': 8080, 'host': '192.168.1.148'})

    flask_thread.start()
