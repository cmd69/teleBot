import os
import threading
from flask import Flask
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

def setup_flask():
    app = Flask(__name__)
    mode = os.environ.get('TELEBOT_ENV', 'dev')  # Default to development mode if not specified

    if mode == 'prod':
        app.config.from_pyfile(os.environ.get('PROD_SETTINGS_FILE'))
    else:
        app.config.from_pyfile(os.environ.get('DEV_SETTINGS_FILE'))

    return app


def run_flask(app):
    ip = app.config["FLASK_IP"]
    if ip == 'prod':
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': 8080, 'host': ip})
    else:
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False, 'port': 8080, 'host': ip})

    flask_thread.start()
